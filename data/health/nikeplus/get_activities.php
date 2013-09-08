#!/usr/bin/php
<?php
	@ini_set("memory_limit",'512M');
	require_once 'nikeplusphp.4.5.php';

	// read configuration
	$config = json_decode(file_get_contents('config.json'), true);

	print "STATUS: Logging in...\n";
	$n = new NikePlusPHP($config['username'], $config['password']);

	//print "Fetchting statistics...\n";
	//$statistics = $n->allTime();
	//file_put_contents("statistics.json", json_encode($statistics));

	print "STATUS: Downloading activities...\n";
	$activities = $n->activities();
	print "STATUS: " . count($activities) . " activities to go.\n";

	$activity_list = array();
	$i = 0;
	foreach($activities as $activity) {
		array_push($activity_list, $n->activity($activity->activityId));
		print "DONE: Downloaded activity " . ++$i . " of " . count($activities) . "...\n";
	}

	file_put_contents("activities.json", json_encode($activity_list));
	print "DONE: Downloaded " . count($activities) . " activities.\n";
?>
