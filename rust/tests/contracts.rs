use std::error::Error;
use std::num::{IntErrorKind, ParseIntError};

use count_import::{parse_counts, CountImportContext};

#[test]
fn simple_parser_handles_empty_input_and_count_boundaries() -> Result<(), ParseIntError> {
    assert_eq!(simple_counts::parse_counts("")?, Vec::<u32>::new());
    assert_eq!(
        simple_counts::parse_counts("0\r\n42\r\n4294967295\r\n")?,
        vec![0, 42, u32::MAX]
    );
    Ok(())
}

#[test]
fn simple_parser_rejects_invalid_counts_without_trimming() {
    for (raw, kind) in [
        ("2\n\n3", IntErrorKind::Empty),
        (" ", IntErrorKind::InvalidDigit),
        ("-1", IntErrorKind::InvalidDigit),
        ("4294967296", IntErrorKind::PosOverflow),
    ] {
        let error = simple_counts::parse_counts(raw).expect_err("invalid count accepted");
        assert_eq!(error.kind(), &kind);
    }
}

#[test]
fn configured_parser_preserves_counts_and_line_endings() -> Result<(), Box<dyn Error>> {
    for skip_empty_records in [false, true] {
        let ctx = CountImportContext { skip_empty_records };
        assert_eq!(parse_counts("", &ctx)?, Vec::<u32>::new());
        assert_eq!(
            parse_counts("0\r\n42\r\n4294967295\r\n", &ctx)?,
            vec![0, 42, u32::MAX]
        );
    }
    Ok(())
}

#[test]
fn empty_records_are_errors_when_skipping_is_disabled() {
    let ctx = CountImportContext {
        skip_empty_records: false,
    };
    let error = parse_counts("2\n\n3", &ctx).expect_err("empty record accepted");
    assert_eq!(error.line, 2);
    assert_eq!(error.source.kind(), &IntErrorKind::Empty);
}

#[test]
fn skip_policy_removes_only_empty_records() -> Result<(), Box<dyn Error>> {
    let ctx = CountImportContext {
        skip_empty_records: true,
    };
    assert_eq!(parse_counts("2\n\n3\n", &ctx)?, vec![2, 3]);
    assert_eq!(parse_counts("\n\r\n", &ctx)?, Vec::<u32>::new());
    let error = parse_counts("2\n\n \n3", &ctx).expect_err("whitespace was trimmed");
    assert_eq!(error.line, 3);
    assert_eq!(error.source.kind(), &IntErrorKind::InvalidDigit);
    Ok(())
}

#[test]
fn neither_flag_setting_bypasses_invalid_counts() {
    for skip_empty_records in [false, true] {
        let ctx = CountImportContext { skip_empty_records };
        for raw in ["x", " ", "-1", "4294967296"] {
            assert!(parse_counts(raw, &ctx).is_err(), "accepted {raw:?}");
        }
    }
}

#[test]
fn errors_retain_original_line_and_typed_source() {
    let ctx = CountImportContext {
        skip_empty_records: true,
    };
    let error = parse_counts("2\n\n4294967296", &ctx).expect_err("overflow accepted");
    assert_eq!(error.line, 3);
    assert_eq!(error.to_string(), "invalid count at line 3");
    let source = error
        .source()
        .and_then(|source| source.downcast_ref::<ParseIntError>())
        .expect("missing typed parsing cause");
    assert_eq!(source.kind(), &IntErrorKind::PosOverflow);
}
