function number_examples() {
    var examples = document.querySelectorAll("li.example");
    for (var exc = 0; exc < examples.length; exc++) {
        ex = examples[exc]
        ex.setAttribute("value", exc + 1)
        var subexamplesol = ex.querySelector("ol.subexample");
        if (subexamplesol) {
            subexamples = subexamplesol.children
            for (var subexc = 0; subexc < subexamples.length; subexc++) {
                subexamples[subexc].setAttribute("value", subexc + 1)
            }
        }
    }

    var exrefs = document.querySelectorAll("a.exref");
    exrefs.forEach(function(x, i) {
        example_id = x.getAttribute("example_id")
        x.setAttribute("href", "#" + example_id)
        x.textContent = "("+get_example_marker(example_id)
        if (x.hasAttribute("end")) {
            end = x.getAttribute("end")
            x.textContent += "-" + get_example_marker(end)
        }
        if (x.hasAttribute("suffix")) {
            x.textContent += x.getAttribute("suffix")
        }
        x.textContent += ")"
    });
}


function get_example_marker(example_id) {
    ex = document.getElementById(example_id)
    parent = ex.parentElement
    if (parent.getAttribute("class") == "subexample") {
        return parent.parentElement.value + String.fromCharCode(96 + ex.value)
    }
    return ex.value
}

function get_number_label(counters, level) {
    output = []
    for (var i = 2; i <= level; i++) {
        output.push(counters["h"+i])
    }
    return output.join(".")
}

var stored = {}

function number_sections(){
    var toc = document.getElementById("toc")
    var title = document.createElement('span')
    toc.classList.add("well")
    toc.classList.add("well-small")
    var counters = {};
    var levels = ["h2", "h3", "h4", "h5", "h6"];
    levels.forEach(function(x, i) {
        counters[x] = 0
    })
    // assuming that there is a single h1!
    h1 = document.querySelectorAll("h1")[0];
    if (h1.hasAttribute("number")) {
        prefix = h1.getAttribute("number") + "."
    } else {
        prefix = ""
    }
    h1.textContent = prefix+" " + h1.textContent
    var headings = document.querySelectorAll("h2, h3, h4, h5, h6");
    headings.forEach(function(heading, i) {
        var level = heading.tagName.toLowerCase();
        counters[level] += 1
        number = get_number_label(counters, level.charAt(level.length - 1))
        heading.textContent = prefix + number + ". " + heading.textContent
        // reset the smaller counters
        reached = false;
        crossref = document.createElement('a')
        crossref.textContent = '\xa0\xa0'.repeat(level.charAt(level.length - 1)-2)+heading.textContent
        crossref.href = "#"+heading.id
        li = document.createElement('div')
        li.appendChild(crossref);
        toc.appendChild(li);
        stored[heading.id] = prefix + number
        levels.forEach(function(level_comp, j) {
            if (reached){
                counters[level_comp] = 0
            };
            if (level==level_comp){
                reached = true;
            }
        });
    });
}

function capitalizeFirstLetter(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}


function number_captions(){
    var captions = document.querySelectorAll("div.caption");
    var kinds = ["table", "figure"]
    var counters = {"table": 0, "figure": 0}
    captions.forEach(function(caption, i) {
        kinds.forEach(function(kind, j) {
            if (caption.classList.contains(kind)){
                counters[kind] += 1
                ref_counter = capitalizeFirstLetter(kind) + " " + counters[kind];
                caption.textContent = ref_counter + ": " + caption.textContent
                stored[caption.id] = ref_counter
            }
        });
    });
    var refs = document.querySelectorAll("a.crossref");
    refs.forEach(function(ref, i) {
        ref.textContent = stored[ref.id]
        ref.id = null
    })
}