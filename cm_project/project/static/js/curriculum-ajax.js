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
	
		$('#add_courses_1').keyup(function(){
		var query;
		query = $(this).val();
		var1 = $("#hidden-input1").val();
		var2 = $("#hidden-input2").val();
		$.get('/curriculum/suggest_course_add_one/', {add_courses_1: query, arg1: var1, arg2: var2}, function(data){
                 $('#results1').html(data);
		});
	});
	
		$('#add_courses_2').keyup(function(){
		var query;
		query = $(this).val();
		var1 = $("#hidden-input3").val();
		var2 = $("#hidden-input4").val();
		$.get('/curriculum/suggest_course_add_two/', {add_courses_2: query, arg1: var1, arg2: var2}, function(data){
                 $('#results2').html(data);
		});
	});
	
		$('#add_courses_3').keyup(function(){
		var query;
		query = $(this).val();
		var1 = $("#hidden-input5").val();
		var2 = $("#hidden-input6").val();
		$.get('/curriculum/suggest_course_add_three/', {add_courses_3: query, arg1: var1, arg2: var2}, function(data){
                 $('#results3').html(data);
		});
	});	
	
		$('#add_courses_4').keyup(function(){
		var query;
		query = $(this).val();
		var1 = $("#hidden-input7").val();
		var2 = $("#hidden-input8").val();
		$.get('/curriculum/suggest_course_add_four/', {add_courses_4: query, arg1: var1, arg2: var2}, function(data){
                 $('#results4').html(data);
		});
	});	
	
		$('#add_pre').keyup(function(){
		var query;
		query = $(this).val();
		var1 = $("#hidden-input-pre").val();
		var2 = $("#hidden-input-pre2").val();
		$.get('/curriculum/suggest_pre_requisite/', {add_pre: query, arg1: var1, arg2: var2}, function(data){
                 $('#resultspre').html(data);
		});
	});	
	
		$('#add_co').keyup(function(){
		var query;
		query = $(this).val();
		var1 = $("#hidden-input-co").val();
		var2 = $("#hidden-input-co2").val();
		$.get('/curriculum/suggest_co_requisite/', {add_co: query, arg1: var1, arg2: var2}, function(data){
                 $('#resultsco').html(data);
		});
	});	
	
		$('#add_anti').keyup(function(){
		var query;
		query = $(this).val();
		var1 = $("#hidden-input-anti").val();
		var2 = $("#hidden-input-anti2").val();
		$.get('/curriculum/suggest_anti_requisite/', {add_anti: query, arg1: var1, arg2: var2}, function(data){
                 $('#resultsanti').html(data);
		});
	});	

});