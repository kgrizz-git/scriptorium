//! Book package `meta.json` types (formatVersion 1).
//!
//! Mirrors [`docs/book-format.schema.json`]. Serde handles wire shape; call
//! [`BookMeta::validate`] after deserialize so cross-field rules the schema
//! cannot express (e.g. `lastReadPage` vs `pages.length`) are enforced.
//!
//! Unknown JSON keys are rejected at deserialize time (`deny_unknown_fields`).

use serde::{Deserialize, Serialize};

/// Book `id` slug pattern — must stay in lockstep with
/// `docs/book-format.schema.json` `properties.id.pattern` and Python `BOOK_ID_RE`.
pub const BOOK_ID_PATTERN: &str = r"^[a-z0-9][a-z0-9._-]{0,63}$";

/// How a book renders. Default is `Scan`.
#[derive(Debug, Clone, Copy, Default, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum RenderMode {
    #[default]
    Scan,
    Text,
    Hybrid,
}

/// How a page is stored. Default is `Copied`.
#[derive(Debug, Clone, Copy, Default, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum StorageMode {
    #[default]
    Copied,
    Referenced,
}

/// Validation failure for a book package `meta.json` document.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum BookMetaError {
    /// `formatVersion` is not the supported major version.
    UnsupportedFormatVersion(u32),
    /// `id` is empty, unsafe as a directory name, or fails the slug pattern.
    InvalidBookId { id: String, reason: String },
    /// `pages` must contain at least one entry.
    EmptyPages,
    /// `lastReadPage` is not a valid 0-based index into `pages`.
    LastReadPageOutOfRange {
        last_read_page: u32,
        page_count: usize,
    },
    /// `pages[i].index` does not equal the array position `i`.
    PageIndexMismatch { position: usize, index: u32 },
    /// A page `file` path is absolute, traverses, or uses disallowed characters.
    InvalidPageFile {
        index: u32,
        file: String,
        reason: String,
    },
    /// Image dimensions must be at least 1×1.
    DegenerateImageSize { index: u32, width: u32, height: u32 },
    /// `byteSize` must be greater than zero.
    ZeroByteSize { index: u32 },
    /// `sha256` must be 64 lowercase hex characters.
    InvalidSha256 { index: u32, sha256: String },
}

impl std::fmt::Display for BookMetaError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::UnsupportedFormatVersion(v) => {
                write!(f, "unsupported formatVersion {v} (expected 1)")
            }
            Self::InvalidBookId { id, reason } => {
                write!(f, "id {id:?} invalid: {reason}")
            }
            Self::EmptyPages => write!(f, "pages must be non-empty"),
            Self::LastReadPageOutOfRange {
                last_read_page,
                page_count,
            } => write!(
                f,
                "lastReadPage {last_read_page} out of range for {page_count} page(s)"
            ),
            Self::PageIndexMismatch { position, index } => {
                write!(f, "pages[{position}].index is {index}, expected {position}")
            }
            Self::InvalidPageFile {
                index,
                file,
                reason,
            } => {
                write!(f, "pages[{index}].file {file:?} invalid: {reason}")
            }
            Self::DegenerateImageSize {
                index,
                width,
                height,
            } => write!(f, "pages[{index}] has degenerate size {width}×{height}"),
            Self::ZeroByteSize { index } => {
                write!(f, "pages[{index}].byteSize must be > 0")
            }
            Self::InvalidSha256 { index, sha256 } => {
                write!(
                    f,
                    "pages[{index}].sha256 {sha256:?} is not 64 lowercase hex"
                )
            }
        }
    }
}

impl std::error::Error for BookMetaError {}

/// One page entry in `meta.json`.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct PageEntry {
    pub index: u32,
    pub file: String,
    pub width: u32,
    pub height: u32,
    pub byte_size: u64,
    pub sha256: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub page_label: Option<String>,
    #[serde(default)]
    pub storage: StorageMode,
}

impl PageEntry {
    /// Validate path safety, dimensions, byte size, and checksum shape for this page.
    pub fn validate(&self) -> Result<(), BookMetaError> {
        validate_page_file(self.index, &self.file)?;
        if self.width < 1 || self.height < 1 {
            return Err(BookMetaError::DegenerateImageSize {
                index: self.index,
                width: self.width,
                height: self.height,
            });
        }
        if self.byte_size == 0 {
            return Err(BookMetaError::ZeroByteSize { index: self.index });
        }
        if !is_lowercase_hex_sha256(&self.sha256) {
            return Err(BookMetaError::InvalidSha256 {
                index: self.index,
                sha256: self.sha256.clone(),
            });
        }
        Ok(())
    }
}

/// Top-level `meta.json` document.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct BookMeta {
    pub format_version: u32,
    pub id: String,
    pub title: String,
    pub created_at: String,
    pub updated_at: String,
    pub render_mode: RenderMode,
    pub last_read_page: u32,
    pub rights: String,
    pub attribution: String,
    pub pages: Vec<PageEntry>,
}

impl BookMeta {
    /// A minimal valid sample for tests and fixtures.
    pub fn sample() -> Self {
        Self {
            format_version: 1,
            id: "sample-book-001".into(),
            title: "Sample Book".into(),
            created_at: "2026-08-24T00:00:00Z".into(),
            updated_at: "2026-08-24T00:00:00Z".into(),
            render_mode: RenderMode::Scan,
            last_read_page: 0,
            rights: "".into(),
            attribution: "".into(),
            pages: vec![PageEntry {
                index: 0,
                file: "pages/000.jpg".into(),
                width: 1200,
                height: 1600,
                byte_size: 245_760,
                // Shape-only digest for structural tests — not the hash of a real 1200×1600 image.
                sha256: "b5bb9d8014a0f9b1d61e21e796d78dccdf1352f23cd32812f4850b878ae4944c".into(),
                page_label: None,
                storage: StorageMode::Copied,
            }],
        }
    }

    /// Enforce rules the JSON Schema cannot express alone.
    ///
    /// Callers that load packages MUST run this (or clamp `last_read_page`)
    /// before trusting the document. Out-of-range `lastReadPage` is rejected
    /// here; UI loaders may alternatively clamp to `pages.len() - 1`.
    pub fn validate(&self) -> Result<(), BookMetaError> {
        if self.format_version != 1 {
            return Err(BookMetaError::UnsupportedFormatVersion(self.format_version));
        }
        validate_book_id(&self.id)?;
        if self.pages.is_empty() {
            return Err(BookMetaError::EmptyPages);
        }
        let page_count = self.pages.len();
        if (self.last_read_page as usize) >= page_count {
            return Err(BookMetaError::LastReadPageOutOfRange {
                last_read_page: self.last_read_page,
                page_count,
            });
        }
        for (position, page) in self.pages.iter().enumerate() {
            if page.index as usize != position {
                return Err(BookMetaError::PageIndexMismatch {
                    position,
                    index: page.index,
                });
            }
            page.validate()?;
        }
        Ok(())
    }
}

/// Book `id` must be a safe library directory slug (matches schema pattern).
fn validate_book_id(id: &str) -> Result<(), BookMetaError> {
    let reason = if id.is_empty() {
        Some("empty id")
    } else if id.len() > 64 {
        Some("longer than 64 characters")
    } else if !id
        .chars()
        .next()
        .is_some_and(|c| c.is_ascii_lowercase() || c.is_ascii_digit())
    {
        Some("must start with a lowercase letter or digit")
    } else if !id
        .chars()
        .all(|c| c.is_ascii_lowercase() || c.is_ascii_digit() || matches!(c, '.' | '_' | '-'))
    {
        Some("only lowercase alnum, '.', '_', '-' allowed")
    } else {
        None
    };

    match reason {
        Some(reason) => Err(BookMetaError::InvalidBookId {
            id: id.to_string(),
            reason: reason.to_string(),
        }),
        None => Ok(()),
    }
}

/// Reject absolute paths, `..` segments, backslashes, and null bytes.
fn validate_page_file(index: u32, file: &str) -> Result<(), BookMetaError> {
    let reason = if file.is_empty() {
        Some("empty path")
    } else if file.contains('\0') {
        Some("contains null byte")
    } else if file.starts_with('/') || file.starts_with('\\') {
        Some("absolute path")
    } else if file.contains('\\') {
        Some("backslash not allowed; use forward slashes")
    } else if file.split('/').any(|seg| seg == ".." || seg.is_empty()) {
        Some("empty or .. path segment")
    } else if !file
        .chars()
        .all(|c| c.is_ascii_alphanumeric() || matches!(c, '.' | '_' | '-' | '/'))
    {
        Some("disallowed characters")
    } else {
        None
    };

    match reason {
        Some(reason) => Err(BookMetaError::InvalidPageFile {
            index,
            file: file.to_string(),
            reason: reason.to_string(),
        }),
        None => Ok(()),
    }
}

fn is_lowercase_hex_sha256(s: &str) -> bool {
    s.len() == 64 && s.chars().all(|c| matches!(c, '0'..='9' | 'a'..='f'))
}

#[cfg(test)]
mod tests {
    use super::*;
    use serde_json::Value;

    fn load_schema() -> Value {
        let schema_path = format!(
            "{}/../docs/book-format.schema.json",
            env!("CARGO_MANIFEST_DIR")
        );
        let schema_str = std::fs::read_to_string(&schema_path)
            .unwrap_or_else(|e| panic!("failed to read schema at {schema_path}: {e}"));
        serde_json::from_str(&schema_str).expect("schema is not valid JSON")
    }

    fn compile_schema(schema: &Value) -> jsonschema::Validator {
        jsonschema::validator_for(schema).expect("schema is not valid")
    }

    #[test]
    fn sample_serialization_matches_schema() {
        let book = BookMeta::sample();
        book.validate().expect("sample must validate");
        let json = serde_json::to_value(&book).unwrap();
        let schema = load_schema();
        let validator = compile_schema(&schema);
        if let Err(error) = validator.validate(&json) {
            panic!("sample did not validate against schema: {error:?}");
        }
    }

    #[test]
    fn page_label_variants_validate() {
        let mut with_label = BookMeta::sample();
        with_label.pages[0].page_label = Some("Cover".into());

        let schema = load_schema();
        let validator = compile_schema(&schema);

        let labeled = serde_json::to_value(&with_label).unwrap();
        assert_eq!(
            labeled["pages"][0]["pageLabel"], "Cover",
            "key must serialize as pageLabel"
        );
        assert!(
            validator.is_valid(&labeled),
            "Some(page_label) variant must validate"
        );

        let unlabeled = serde_json::to_value(&BookMeta::sample()).unwrap();
        assert!(
            unlabeled["pages"][0].get("pageLabel").is_none(),
            "None must be omitted"
        );
        assert!(validator.is_valid(&unlabeled), "None variant must validate");
    }

    #[test]
    fn schema_rejects_missing_required_field() {
        let book = BookMeta::sample();
        let mut json = serde_json::to_value(&book).unwrap();
        json.as_object_mut().unwrap().remove("title");
        let schema = load_schema();
        let validator = compile_schema(&schema);
        assert!(
            !validator.is_valid(&json),
            "schema should reject a missing required field"
        );
    }

    #[test]
    fn schema_rejects_zero_dimensions() {
        let mut book = BookMeta::sample();
        book.pages[0].width = 0;
        let json = serde_json::to_value(&book).unwrap();
        let validator = compile_schema(&load_schema());
        assert!(!validator.is_valid(&json), "width 0 must fail schema");
    }

    #[test]
    fn schema_rejects_path_traversal_file() {
        let mut book = BookMeta::sample();
        book.pages[0].file = "../etc/passwd".into();
        let json = serde_json::to_value(&book).unwrap();
        let validator = compile_schema(&load_schema());
        assert!(!validator.is_valid(&json), "../ path must fail schema");
        assert!(book.pages[0].validate().is_err());
    }

    #[test]
    fn schema_rejects_terminal_parent_segment() {
        let validator = compile_schema(&load_schema());
        for bad in ["..", "pages/.."] {
            let mut book = BookMeta::sample();
            book.pages[0].file = bad.into();
            let json = serde_json::to_value(&book).unwrap();
            assert!(
                !validator.is_valid(&json),
                "schema must reject terminal .. path {bad:?}"
            );
            assert!(
                book.pages[0].validate().is_err(),
                "Rust must reject terminal .. path {bad:?}"
            );
        }
    }

    #[test]
    fn schema_rejects_integer_above_u32() {
        let book = BookMeta::sample();
        let mut json = serde_json::to_value(&book).unwrap();
        json["pages"][0]["width"] = serde_json::json!(4_294_967_296u64);
        let validator = compile_schema(&load_schema());
        assert!(
            !validator.is_valid(&json),
            "width above u32::MAX must fail schema"
        );
    }

    #[test]
    fn validate_rejects_last_read_page_out_of_range() {
        let mut book = BookMeta::sample();
        book.last_read_page = 999;
        match book.validate() {
            Err(BookMetaError::LastReadPageOutOfRange { .. }) => {}
            other => panic!("expected LastReadPageOutOfRange, got {other:?}"),
        }
    }

    #[test]
    fn validate_rejects_invalid_book_id() {
        let validator = compile_schema(&load_schema());
        for bad in ["", "../etc", "Has Caps", ".", "bad/id"] {
            let mut book = BookMeta::sample();
            book.id = bad.into();
            assert!(
                matches!(book.validate(), Err(BookMetaError::InvalidBookId { .. })),
                "Rust must reject id {bad:?}"
            );
            let json = serde_json::to_value(&book).unwrap();
            assert!(!validator.is_valid(&json), "schema must reject id {bad:?}");
        }
    }

    #[test]
    fn validate_rejects_zero_byte_size() {
        let mut book = BookMeta::sample();
        book.pages[0].byte_size = 0;
        match book.validate() {
            Err(BookMetaError::ZeroByteSize { .. }) => {}
            other => panic!("expected ZeroByteSize, got {other:?}"),
        }
        let json = serde_json::to_value(&book).unwrap();
        let validator = compile_schema(&load_schema());
        assert!(!validator.is_valid(&json), "schema must reject byteSize 0");
    }

    #[test]
    fn book_id_pattern_matches_schema() {
        let schema = load_schema();
        let pattern = schema["properties"]["id"]["pattern"]
            .as_str()
            .expect("schema id.pattern must be a string");
        assert_eq!(
            pattern, BOOK_ID_PATTERN,
            "Rust BOOK_ID_PATTERN must match docs/book-format.schema.json"
        );
    }

    #[test]
    fn deserialize_rejects_unknown_top_level_field() {
        let mut json = serde_json::to_value(BookMeta::sample()).unwrap();
        json.as_object_mut()
            .unwrap()
            .insert("unknownField".into(), serde_json::json!(1));
        assert!(
            serde_json::from_value::<BookMeta>(json).is_err(),
            "unknown top-level keys must fail deserialize"
        );
    }

    #[test]
    fn deserialize_rejects_unknown_page_field() {
        let mut json = serde_json::to_value(BookMeta::sample()).unwrap();
        json["pages"][0]["extra"] = serde_json::json!("nope");
        assert!(
            serde_json::from_value::<BookMeta>(json).is_err(),
            "unknown page keys must fail deserialize"
        );
    }

    #[test]
    fn validate_rejects_unsupported_format_version() {
        let mut book = BookMeta::sample();
        book.format_version = 2;
        match book.validate() {
            Err(BookMetaError::UnsupportedFormatVersion(2)) => {}
            other => panic!("expected UnsupportedFormatVersion(2), got {other:?}"),
        }
    }

    #[test]
    fn validate_rejects_empty_pages() {
        let mut book = BookMeta::sample();
        book.pages.clear();
        match book.validate() {
            Err(BookMetaError::EmptyPages) => {}
            other => panic!("expected EmptyPages, got {other:?}"),
        }
    }

    #[test]
    fn validate_page_file_rejects_unsafe_paths() {
        let cases = [
            ("", "empty path"),
            ("/etc/passwd", "absolute path"),
            (r"pages\000.jpg", "backslash"),
            ("a//b", "empty segment"),
            ("pages/..", "parent segment"),
            ("pages/foo bar.jpg", "space"),
            ("pages/foo:bar.jpg", "colon"),
            ("pages/über.jpg", "non-ascii"),
        ];
        for (file, label) in cases {
            match validate_page_file(0, file) {
                Err(BookMetaError::InvalidPageFile { .. }) => {}
                other => panic!("{label} path {file:?} should fail, got {other:?}"),
            }
        }
    }

    #[test]
    fn validate_page_file_rejects_null_byte() {
        let file = format!("pages/{}\0.jpg", 'a');
        match validate_page_file(0, &file) {
            Err(BookMetaError::InvalidPageFile { reason, .. }) => {
                assert!(reason.contains("null byte"), "reason: {reason}");
            }
            other => panic!("expected InvalidPageFile for null byte, got {other:?}"),
        }
    }

    #[test]
    fn validate_accepts_wrong_sha256_shape_only() {
        let mut book = BookMeta::sample();
        book.pages[0].sha256 =
            "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb".into();
        book.pages[0]
            .validate()
            .expect("PageEntry only checks sha256 shape, not file bytes");
        book.validate()
            .expect("BookMeta::validate does not verify sha256 against files (M1 load_book must)");
    }

    #[test]
    fn validate_rejects_page_index_mismatch_cases() {
        let good_sha = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";

        let mut ok = BookMeta::sample();
        ok.pages.push(PageEntry {
            index: 1,
            file: "pages/001.jpg".into(),
            width: 100,
            height: 100,
            byte_size: 10,
            sha256: good_sha.into(),
            page_label: None,
            storage: StorageMode::Copied,
        });
        ok.validate().expect("contiguous indexes 0,1 must pass");

        let mut dupes = BookMeta::sample();
        dupes.pages.push(PageEntry {
            index: 0,
            file: "pages/001.jpg".into(),
            width: 100,
            height: 100,
            byte_size: 10,
            sha256: good_sha.into(),
            page_label: None,
            storage: StorageMode::Copied,
        });
        match dupes.validate() {
            Err(BookMetaError::PageIndexMismatch {
                position: 1,
                index: 0,
            }) => {}
            other => panic!("duplicate indexes should fail at position 1, got {other:?}"),
        }

        let mut gap = BookMeta::sample();
        gap.pages.push(PageEntry {
            index: 2,
            file: "pages/002.jpg".into(),
            width: 100,
            height: 100,
            byte_size: 10,
            sha256: good_sha.into(),
            page_label: None,
            storage: StorageMode::Copied,
        });
        match gap.validate() {
            Err(BookMetaError::PageIndexMismatch {
                position: 1,
                index: 2,
            }) => {}
            other => panic!("gap at index 2 should fail at position 1, got {other:?}"),
        }

        let mut huge = BookMeta::sample();
        huge.pages.push(PageEntry {
            index: u32::MAX,
            file: "pages/huge.jpg".into(),
            width: 100,
            height: 100,
            byte_size: 10,
            sha256: good_sha.into(),
            page_label: None,
            storage: StorageMode::Copied,
        });
        match huge.validate() {
            Err(BookMetaError::PageIndexMismatch { position: 1, index }) if index == u32::MAX => {}
            other => panic!("huge index at position 1 should fail, got {other:?}"),
        }
    }

    #[test]
    fn storage_referenced_deserializes() {
        let json = serde_json::json!({
            "formatVersion": 1,
            "id": "ref-book",
            "title": "Referenced",
            "createdAt": "2026-08-24T00:00:00Z",
            "updatedAt": "2026-08-24T00:00:00Z",
            "renderMode": "scan",
            "lastReadPage": 0,
            "rights": "",
            "attribution": "",
            "pages": [{
                "index": 0,
                "file": "pages/000.png",
                "width": 100,
                "height": 100,
                "byteSize": 12,
                "sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "storage": "referenced"
            }]
        });
        let book: BookMeta = serde_json::from_value(json).expect("deserialize");
        assert_eq!(book.pages[0].storage, StorageMode::Referenced);
        book.validate().expect("referenced storage is schema-valid");
        let validator = compile_schema(&load_schema());
        assert!(validator.is_valid(&serde_json::to_value(&book).unwrap()));
    }

    #[test]
    fn fixture_generator_meta_round_trips_through_rust_types() {
        let root = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("..");
        let out = root.join("tmp/fixtures/rust-roundtrip-book");
        let _ = std::fs::remove_dir_all(&out);
        std::fs::create_dir_all(&out).expect("create out dir");

        let status = std::process::Command::new("python3")
            .arg(root.join("scripts/generate-fixture-book.py"))
            .arg("--pages")
            .arg("2")
            .arg("--seed")
            .arg("7")
            .arg("--out")
            .arg(&out)
            .current_dir(&root)
            .status()
            .expect("spawn fixture generator");
        assert!(status.success(), "fixture generator failed: {status}");

        let meta_path = out.join("meta.json");
        let meta_str = std::fs::read_to_string(&meta_path).expect("read meta.json");
        let book: BookMeta = serde_json::from_str(&meta_str).expect("deserialize fixture meta");
        book.validate()
            .expect("fixture must pass BookMeta::validate");

        let re_serialized = serde_json::to_value(&book).expect("re-serialize");
        let original: Value = serde_json::from_str(&meta_str).expect("parse original JSON");
        assert_eq!(
            re_serialized, original,
            "Rust round-trip must preserve fixture meta.json"
        );

        let validator = compile_schema(&load_schema());
        assert!(
            validator.is_valid(&re_serialized),
            "round-tripped meta must match schema"
        );
    }
}
