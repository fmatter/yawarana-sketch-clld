<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%from clld_markdown_plugin import markdown%>
<%! active_menu_item = "documents" %>
<% ex_cnt = 0 %>



<article>
% if ctx.chapter_no:
    <% no_str = f" number={ctx.chapter_no}"%>
% else:
    <% no_str = ""%>
% endif

<h1${no_str}>${ctx.name}</h1>

${markdown(request, ctx.description, permalink=False)[0]|n}

</article>

