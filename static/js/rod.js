<script>
    var user = JSON.parse('{{ json_data | tojson | safe}}');
    console.log(user)

// Store
sessionStorage.setItem("lastname", "Smith");
// Retrieve
document.getElementById("result").innerHTML = sessionStorage.getItem("lastname");

</script>