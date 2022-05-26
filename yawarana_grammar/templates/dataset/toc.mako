<%from clld_markdown_plugin import markdown%>
<%from clld.db.meta import DBSession%>
<%from yawarana_grammar.models import Document%>

<% chapter_strings = [] %>
% for chapter in DBSession.query(Document).filter(Document.chapter_no!=None):
<% chapter_strings.append(f"1. [](ChapterTable#cldf:{chapter.id})") %>
% endfor
<% chapter_strings = "\n".join(chapter_strings) %>

${markdown(request, f"""
#### Table of contents
{chapter_strings}
""")[0]|n}

