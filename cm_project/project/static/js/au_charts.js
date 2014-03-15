$(document).ready(function(){
				// ~~ PIECHART ~~
				var pie_data = [
					  {
					  value: {{ es_total }},
					  color:"#35324F"
					  },
					  {
					  value : {{ ed_total }},
					  color : "#7D0541"
					  },
					  {
					  value : {{ ma_total }},
					  color : "#8EC0FF"
					  },
					  {
					  value : {{ sc_total }},
					  color : "#617992"
					  },
					  {
					  value : {{ co_total }},
					  color : "#FFA62F"
					  }
				]
				pie_options = {
				//Boolean - Whether we should show a stroke on each segment
				segmentShowStroke : true,
				
				//String - The colour of each segment stroke
				segmentStrokeColor : "#fff",
				
				//Number - The width of each segment stroke
				segmentStrokeWidth : 2,
				
				//Boolean - Whether we should animate the chart
				animation : true,
				
				//Number - Amount of animation steps
				animationSteps : 100,
				
				//String - Animation easing effect
				animationEasing : "easeOutBounce",
				
				//Boolean - Whether we animate the rotation of the Pie
				animateRotate : true,
				
				//Boolean - Whether we animate scaling the Pie from the centre
				animateScale : false,
				
				//Function - Will fire on animation completion.
				onAnimationComplete : null
				}
				
				//Get the context of the canvas element we want to select
				var pie_ctx = document.getElementById("pieChartTotal").getContext("2d");
				var pie_chart = new Chart(pie_ctx).Pie(pie_data);
				new Chart(pie_ctx).Pie(pie_data,pie_options);
	   
				  
});