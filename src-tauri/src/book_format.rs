use serde::{Deserialize, Serialize};

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

/// One page entry in `meta.json`.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
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

/// Top-level `meta.json` document.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
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
                sha256: "b5bb9d8014a0f9b1d61e21e796d78dccdf1352f23cd32812f4850b878ae4944c".into(),
                page_label: None,
                storage: StorageMode::Copied,
            }],
        }
    }
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
        // Remove a required top-level field.
        json.as_object_mut().unwrap().remove("title");
        let schema = load_schema();
        let validator = compile_schema(&schema);
        assert!(
            !validator.is_valid(&json),
            "schema should reject a missing required field"
        );
    }
}
