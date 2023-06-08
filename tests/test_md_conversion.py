from sglmr.utils import render_md


def test_footnote_conversion():
    md = "test[^1]\n\n[^1]:my-footnote"
    content = render_md(md)
    
    assert 'class="footnote' in content
    assert 'href="#' in content
    assert "test" in content
    assert "my-footnote" in content