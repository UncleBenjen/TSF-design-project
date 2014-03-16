$(document).ready(function() {

    	$('#course_suggestion').keyup(function(){
		var query;
		query = $(this).val();
		$.get('/curriculum/suggest_course/', {course_suggestion: query}, function(data){
                 $('#courses').html(data);
		});
	});
	
		$('#concept_suggestion').keyup(function(){
		var query;
		query = $(this).val();
		$.get('/curriculum/suggest_concept/', {concept_suggestion: query}, function(data){
                 $('#concepts').html(data);
		});
	});
	
		$('#link_concept').keyup(function(){
		var query;
		query = $(this).val();
		var1 = $("#hidden-input1").val();
		var2 = $("#hidden-input2").val();
		$.get('/curriculum/suggest_concept_add/', {link_concept: query, arg1: var1, arg2: var2}, function(data){
                 $('#results').html(data);
		});
	});
	
		$('#link_child').keyup(function(){
		var query;
		query = $(this).val();
		var1 = $("#hidden-input1").val();
		$.get('/curriculum/suggest_child_concept_add/', {link_child: query, arg1: var1}, function(data){
                 $('#results').html(data);
		});
	});

});