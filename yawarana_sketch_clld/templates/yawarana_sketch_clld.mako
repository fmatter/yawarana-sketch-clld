<%inherit file="app.mako"/>

##
## define app-level blocks:
##
<%block name="header">
    ##<a href="${request.route_url('dataset')}">
    ##    <img src="${request.static_url('yawarana_sketch_clld:static/header.gif')}"/>
    ##</a>
</%block>

${next.body()}

<%block name="footer_citation">
    ${request.dataset.formatted_name()}
    by
    <span xmlns:cc="http://creativecommons.org/ns#"
          property="cc:attributionName"
          rel="cc:attributionURL">
        ${request.dataset.formatted_editors()}
    </span>
</%block>

<script>
src="${req.static_url('yawarana_sketch_clld:static/project.js')}"
number_examples()
number_captions()
</script>
