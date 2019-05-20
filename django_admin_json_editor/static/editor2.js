var container = document.getElementById("{{ name }}_editor");
var options = {{ editor_options|safe }};
var {{ name }}_editor = new JSONEditor(container, options);
JSONEditor.plugins.sceditor.emoticonsEnabled = {{ sceditor }};
{{ name }}_editor.on('change', function () {
    var errors = {{ name }}_editor.validate();
    if (errors.length) {
        console.log(errors);
    }
    else {
        var json = {{ name }}_editor.getValue();
        // Maybe add autoescape here? I don't think that will fix /script>
        document.getElementById("id_{{ name }}").value = JSON.stringify(json);
    }
});
// forsure bug is here when data is < /script>
{% if data %} // if the value map is not empty
    var json = {{ data|safe }}; // Not escape - also removed |safe and it was really wrong`
    console.log("editor.html - json")
    console.log(json);
    {{ name }}_editor.setValue(json); // hm it puts every in there
{% endif %}
