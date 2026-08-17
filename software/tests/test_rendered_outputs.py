"""Tests for the repository-level rendered-output projection."""

from src.publish.rendered_outputs import copy_course_rendered_outputs


def test_copy_course_rendered_outputs_rebuilds_stable_course_projection(tmp_path):
    repo = tmp_path / "repo"
    course = repo / "course_development" / "biol-1"
    module_output = course / "course" / "module-01-study-of-life" / "output" / "pdf"
    module_output.mkdir(parents=True)
    (module_output / "module-01-key-points.pdf").write_bytes(b"pdf")
    (course / "course" / "module.toml").parent.mkdir(exist_ok=True)
    (course / "course" / "module.toml").write_text("source", encoding="utf-8")

    result = copy_course_rendered_outputs(repo, course, "biol-1")
    projected = repo / "output" / "biol-1" / "course" / "module-01-study-of-life" / "pdf"

    assert result["count"] == 1
    assert (projected / "module-01-key-points.pdf").read_bytes() == b"pdf"
    assert not (repo / "output" / "biol-1" / "course" / "module.toml").exists()


def test_copy_course_rendered_outputs_removes_stale_projection(tmp_path):
    repo = tmp_path / "repo"
    course = repo / "course_development" / "biol-1"
    output = course / "course" / "labs" / "output" / "pdf"
    output.mkdir(parents=True)
    (output / "lab-01.pdf").write_bytes(b"pdf")
    stale = repo / "output" / "biol-1" / "stale.txt"
    stale.parent.mkdir(parents=True)
    stale.write_text("stale", encoding="utf-8")

    copy_course_rendered_outputs(repo, course, "biol-1")

    assert not stale.exists()
    assert (repo / "output" / "biol-1" / "course" / "labs" / "pdf" / "lab-01.pdf").exists()
