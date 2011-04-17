$(function(){
	$(".expand").toggle(function(e){
		$(this).parents("article").find(".detail").show('normal');
		$(this).find(".indicator").html("&laquo;");
		e.preventDefault();
	}, function(e){
		$(this).parents("article").find(".detail").hide('normal');
		$(this).find(".indicator").html("&raquo;");
		e.preventDefault();
	});
});
