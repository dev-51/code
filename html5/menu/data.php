<?php 
$sub_menu = array("submenu" =>
	array(			  
		array(
			"title" => "Clothe",
			"url" => "/clothe.html"
		),
		array(
			"title" =>"Electronic",
			"url" => "/electronic.html"
		),
		array(
			"title" => "Health",
			"url" =>"/health.html"
		),
		array(
			"title" => "Food",
			"url" => "/food.html"
		),
		array(
			"title" => "Others",
			"url" => "/others.html"
		)
	)	
);

print(json_encode($sub_menu));