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

});