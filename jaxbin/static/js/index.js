$(function () {
    $('#jaxInput').on('keyup', function () {
        var jaxValue = $('#jaxInput').val();

        jaxValue = jaxValue.replace(/(?:\r\n|\r|\n)/g, '<br>');

        $('.renderJax').html(jaxValue);
        MathJax.Hub.queue.Push(["Typeset", MathJax.Hub, "renderJax"]);
    });

    var hostname = window.location.hostname;

    $("#createBin").click(function () {
        var binData = $('#jaxInput').val();

        $.ajax({
            type: "POST",
            url: "/createBin",
            data: {
                "binData": binData
            },

            success: function (data) {
                $("#binLink").html("Bin Created: <a target='_blank' href='/bin/" + data + "'>http://" + hostname + "/bin/" + data + "</a>");
            },

            error: function () {
                alert('ohno');
            }
        });
    });
});
