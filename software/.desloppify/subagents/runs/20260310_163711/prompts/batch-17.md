You are a focused subagent reviewer for a single holistic investigation batch.

Repository root: /Users/4d/Documents/GitHub/cr-bio/software
Blind packet: /Users/4d/Documents/GitHub/cr-bio/software/.desloppify/review_packet_blind.json
Batch index: 17
Batch name: contract_coherence
Batch rationale: seed files for contract_coherence review

DIMENSION TO EVALUATE:

## contract_coherence
Functions and modules that honor their stated contracts
Look for:
- Return type annotation lies: declared type doesn't match all return paths
- Docstring/signature divergence: params described in docs but not in function signature
- Functions named getX that mutate state (side effect hidden behind getter name)
- Module-level API inconsistency: some exports follow a pattern, one doesn't
- Error contracts: function says it throws but silently returns None, or vice versa
Skip:
- Protocol/interface stubs (abstract methods with placeholder returns)
- Test helpers where loose typing is intentional
- Overloaded functions with multiple valid return types

YOUR TASK: Read the code for this batch's dimension. Judge how well the codebase serves a developer from that perspective. The dimension rubric above defines what good looks like. Cite specific observations that explain your judgment.

Mechanical scan evidence — navigation aid, not scoring evidence:
The blind packet contains `holistic_context.scan_evidence` with aggregated signals from all mechanical detectors — including complexity hotspots, error hotspots, signal density index, boundary violations, and systemic patterns. Use these as starting points for where to look beyond the seed files.

Seed files (start here):
- src/publish/utils.py
- src/lab_manual/utils.py
- src/format_conversion/utils.py
- src/file_validation/utils.py
- src/legacy_import/utils.py
- src/validation/utils.py
- src/content_processing/utils.py
- src/module_organization/utils.py
- src/schedule/utils.py
- src/batch_processing/utils.py
- src/html_website/utils.py
- src/text_to_speech/utils.py
- src/speech_to_text/utils.py
- src/canvas_integration/utils.py
- src/markdown_to_pdf/utils.py
- src/lab_manual/main.py
- src/html_website/main.py
- src/validation/main.py
- src/publish/main.py
- src/batch_processing/main.py
- scripts/generate_all_outputs.py
- src/markdown_to_pdf/main.py
- src/module_organization/main.py
- src/batch_processing/__init__.py
- src/canvas_integration/__init__.py
- src/content_processing/__init__.py
- src/file_validation/__init__.py
- src/format_conversion/__init__.py
- src/lab_manual/__init__.py
- src/legacy_import/__init__.py
- src/markdown_to_pdf/__init__.py
- src/module_organization/__init__.py
- src/publish/__init__.py
- src/schedule/__init__.py
- src/speech_to_text/__init__.py
- src/text_to_speech/__init__.py
- src/validation/__init__.py
- scripts/flatten_published.py
- scripts/renumber_questions.py
- src/canvas_integration/main.py
- scripts/validate_outputs.py
- scripts/publish_all.py
- scripts/import_legacy_materials.py
- src/legacy_import/main.py
- src/file_validation/main.py

Task requirements:
1. Read the blind packet's `system_prompt` — it contains scoring rules and calibration.
2. Start from the seed files, then freely explore the repository to build your understanding.
3. Keep issues and scoring scoped to this batch's dimension.
4. Respect scope controls: do not include files/directories marked by `exclude`, `suppress`, or non-production zone overrides.
5. Return 0-10 issues for this batch (empty array allowed).
6. Complete `dimension_judgment` for your dimension — all three fields (strengths, issue_character, score_rationale) are required. Write the judgment BEFORE setting the score.
7. Do not edit repository files.
8. Return ONLY valid JSON, no markdown fences.

Scope enums:
- impact_scope: "local" | "module" | "subsystem" | "codebase"
- fix_scope: "single_edit" | "multi_file_refactor" | "architectural_change"

Output schema:
{
  "batch": "contract_coherence",
  "batch_index": 17,
  "assessments": {"<dimension>": <0-100 with one decimal place>},
  "dimension_notes": {
    "<dimension>": {
      "evidence": ["specific code observations"],
      "impact_scope": "local|module|subsystem|codebase",
      "fix_scope": "single_edit|multi_file_refactor|architectural_change",
      "confidence": "high|medium|low",
      "issues_preventing_higher_score": "required when score >85.0",
      "sub_axes": {"abstraction_leverage": 0-100, "indirection_cost": 0-100, "interface_honesty": 0-100, "delegation_density": 0-100, "definition_directness": 0-100, "type_discipline": 0-100}  // required for abstraction_fitness when evidence supports it; all one decimal place
    }
  },
  "dimension_judgment": {
    "<dimension>": {
      "strengths": ["0-5 specific things the codebase does well from this dimension's perspective"],
      "issue_character": "one sentence characterizing the nature/pattern of issues from this dimension's perspective",
      "score_rationale": "2-3 sentences explaining the score from this dimension's perspective, referencing global anchors"
    }
  },
  "issues": [{
    "dimension": "<dimension>",
    "identifier": "short_id",
    "summary": "one-line defect summary",
    "related_files": ["relative/path.py"],
    "evidence": ["specific code observation"],
    "suggestion": "concrete fix recommendation",
    "confidence": "high|medium|low",
    "impact_scope": "local|module|subsystem|codebase",
    "fix_scope": "single_edit|multi_file_refactor|architectural_change",
    "root_cause_cluster": "optional_cluster_name_when_supported_by_history"
  }],
  "retrospective": {
    "root_causes": ["optional: concise root-cause hypotheses"],
    "likely_symptoms": ["optional: identifiers that look symptom-level"],
    "possible_false_positives": ["optional: prior concept keys likely mis-scoped"]
  }
}
