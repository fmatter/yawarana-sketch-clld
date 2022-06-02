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
<div id="docnav">
    <div id="toc" class="well well-small">
    </div>
    <div class="pagination">
        <ul>
            % if ctx.preceding:
                <li><a class="page-link" href="${request.resource_url(ctx.preceding)}">←${ctx.preceding}</a></li>
            % endif
            % if ctx.following:
                <li><a class="page-link" href="${request.resource_url(ctx.following[0])}">${ctx.following[0]}→</a></li>
            % endif
        </ul>
    </div>
</div>

${markdown(request, ctx.description, permalink=False)|n}

</article>

<script>
src="${req.static_url('yawarana_sketch_clld:static/project.js')}"
number_sections()
</script>