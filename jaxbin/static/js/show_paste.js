$(function () {
    jaxValue = $(".bin").html();

    binText = jaxValue.replace(/(?:\r\n|\r|\n)/g, '<br>');
    $(".bin").html(binText);
});
