<?php

/**
 * A PHP class that makes it easy to get your data from the Nike+ service 
 * 
 * Nike+PHP v4.x requires PHP 5 with SimpleXML and cURL.
 * Nike+PHP also requires your Nike log in credentials.
 * 
 * @author Charanjit Chana - http://charanj.it
 * @link http://nikeplusphp.org
 * @version 4.5
 * 
 * Usage:
 * $n = new NikePlusPHP('email@address.com', 'password');
 * $activities = $n->activities();
 * $activity = $n->activity('1234567890');
 *
 * For more examples, visit: http://nikeplusphp.org/#examples
 */

class NikePlusPHP {

	/**
	 * Public variables
	 */
	public $loginCookies, $userId, $activities = false, $allTime = false, $routes = false;

	/**
	 * Private variables
	 */
	private $_cookie, $_userAgent = 'Mozilla/5.0';

	/**
	 * __construct()
	 * Called when you initiate the class and keeps a cookie that allows you to keep authenticating
	 * against the Nike+ website.
	 * 
	 * @param string $username your Nike username, should be an email address
	 * @param string $password your Nike password 
	 */
	public function __construct($username, $password) {
		$this->_login($username, $password);
	}

	/**
	 * _login()
	 * Called by __construct and performs the actual login action.
	 * 
	 * @param string $username
	 * @param string $password
	 * 
	 * @return string
	 */
	private function _login($username, $password) {
		$url = 'https://secure-nikeplus.nike.com/nsl/services/user/login?app=b31990e7-8583-4251-808f-9dc67b40f5d2&format=json&contentType=plaintext';
		$loginDetails = 'app=b31990e7-8583-4251-808f-9dc67b40f5d2&format=json&contentType=plaintext&email='.urlencode($username).'&password='.$password;
		$ch = curl_init();
		$allHeaders = array();
		curl_setopt($ch, CURLOPT_HEADER, true);
		curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
		curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 0);
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, true); //Set curl to return the data instead of printing it to the browser.
		curl_setopt($ch, CURLOPT_POSTFIELDS, $loginDetails);
		curl_setopt($ch, CURLOPT_URL, $url);
		$data = curl_exec($ch);
		curl_close($ch);
		$noDoubleBreaks = str_replace(array("\n\r\n\r", "\r\n\r\n", "\n\n", "\r\r", "\n\n\n\n", "\r\r\r\r"), '||', $data);
		$sections = explode('||', $noDoubleBreaks);
		$headerSections = explode('Set-Cookie: ', $sections[0]);
		$body = $sections[1];
		for($i=1; $i<=count($headerSections); $i++) {
			$allHeaders[] = @str_replace(array("\n\r", "\r\n", "\r", "\n\n", "\r\r"), "", $headerSections[$i]);
		}
		foreach($allHeaders as $h) {
			$exploded[] = explode('; ', $h);
		}
		foreach($exploded as $e) {
			$string[] = $e[0];
		}
		$header = implode(';', $string);
		$this->_cookie = $header;
		$this->loginCookies = json_decode($body);
		$this->userId = $this->loginCookies->serviceResponse->body->User->screenName;
		$this->allTime();
	}

	/**
	 * cookieValue()
	 * returns the cookie value that has been set 
	 */
	public function cookieValue() {
		return $this->_cookie;
	}

	/**
	 * _getNikePlusFile()
	 * collects the contents of the specified file from Nike+
	 * 
	 * @param string $path the file you wish to fetch
	 */
	private function _getNikePlusFile($path) {
		$_SERVER['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest';
		$ch = curl_init();
		curl_setopt($ch, CURLOPT_HEADER, false);
		curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
		curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
		curl_setopt($ch, CURLOPT_COOKIE, $this->_cookie);
		curl_setopt($ch, CURLOPT_USERAGENT, $this->_userAgent);
		curl_setopt($ch, CURLOPT_URL, $path);
		$data = curl_exec($ch);
		curl_close($ch);
		$jsonData = json_decode(utf8_decode($data));
		if(is_null($jsonData)) {
			$jsonData = json_decode($data);
		}
		return $jsonData;
	}

	/**
	 * activities()
	 * a list of your activities
	 *
	 * @param int $limit optional - return a set number of activities, 0 = get all
	 * @param boolean $checkTotal optional - check that a previous call has retrieved all runs
	 *
	 * @return object
	 */
	public function activities($limit = 0, $checkTotal = false) {
		$start = 0;
		$increment = 399;
		$loop = true;
		if($limit == 0) {
			$limit = $increment;
		} else {
			--$limit;
		}
		if($limit != count($this->activities) ||($checkTotal && ($this->activities && count($this->activities) < $this->allTime->lifetimeTotals->run))) {
			$this->activities = false;
		}
		if(!$this->activities) {
			while($loop == true) {
				$results = $this->_getNikePlusFile('http://nikeplus.nike.com/plus/activity/running/'.rawurlencode($this->userId).'/lifetime/activities?indexStart='.$start.'&indexEnd='.$limit);
				if(isset($results->activities)) {
					foreach($results->activities as $activity) {
						$this->activities[$activity->activity->activityId] = $activity->activity;
					}
					$start += $increment + 1;
					$limit += $start;
				} else {
					$loop = false;
					break;
				}
			}
		}
		krsort($this->activities);
		return $this->activities;
	}

	/**
	 * allTime()
	 * a list of your all time stats 
	 *
	 * @return object
	 */
	 public function allTime() {
		if(!$this->allTime) {
			$this->allTime = $this->_getNikePlusFile('http://nikeplus.nike.com/plus/activity/running/'.rawurlencode($this->userId).'/lifetime/activities?indexStart=999999&indexEnd=1000000');
		}
		return $this->allTime;
	}

	/**
	 * activity()
	 * collects the data of a specific activity
	 * 
	 * @param string $id the id of the activity you wish to get the data for
	 *
	 * @return object
	 */
	public function activity($id) {
		return $this->_getNikePlusFile('http://nikeplus.nike.com/plus/running/ajax/'.$id);//->activity;
	}

	/**
	 * mostRecentActivity()
	 * collects the data of the latest activity
	 * 
	 * @return object
	 */
	public function mostRecentActivity() {
		$activities = $this->activities();
		return $this->activity(reset($activities)->activityId);
	}

	/**
	 * firstActivity()
	 * collects the data of the first activity
	 * 
	 * @return object
	 */
	public function firstActivity() {
		$activities = $this->activities(0, true);
		return $this->activity(end($activities)->activityId);
	}

	/**
	 * routes()
	 * a list of your routes
	 *
	 * @return object
	 */
	public function routes() {
		if(!$this->routes) {
			$this->routes = $this->_getNikePlusFile('http://nikeplus.nike.com/location/services/v1.0/routes/running/favorite');
		}
		return $this->routes;
	}

	/**
	 * route()
	 * collects the data of a specific route
	 * 
	 * @param string $id the id of the route you wish to get the data for
	 *
	 * @return object
	 */
	public function route($id) {
		return $this->_getNikePlusFile('http://nikeplus.nike.com/location/services/v1.0/routes/running/'.$id);
	}

	/**
	 * toMiles()
	 * Convert a value from Km in to miles
	 * 
	 * @param float|string $distance
	 * @param int $decimalPlaces optional - set the number of decimal places (default is 2), use to improve granularity
	 * 
	 * @return int
	 */
	public function toMiles($distance, $decimalPlaces = 2) {
		return $this->toTwoDecimalPlaces((float) $distance * 0.6213711922, $decimalPlaces);
	}

	/**
	 * toHours()
	 * convert a value to hours
	 *
	 * @param float $time
	 *
	 * @return string
	 */
	public function toHours($time) {
		return intval($time / 3600000) % 60;
	}

	/**
	 * toMinutes()
	 * convert a value to minutes
	 *
	 * @param float $time
	 *
	 * @return string
	 */
	public function toMinutes($time) {
		return intval($time / 60000) % 60;
	}

	/**
	 * toSeconds()
	 * convert a value to seconds
	 *
	 * @param float $time
	 *
	 * @return string
	 */
	public function toSeconds($time) {
		return intval($time / 1000) % 60;
	}

	/**
	 * padNumber()
	 * pad numbers less than 10 to have a leading 0
	 * 
	 * @param int $number
	 * 
	 * @return string
	 */
	public function padNumber($number){
		if($number < 10 && $number >= 0) {
			return '0'.$number;
		}
		return $number;
	}

	/**
	 * formatDuration()
	 * convert a duration into minutes and seconds, or
	 * hours, minutes and seconds if hours are available
	 *
	 * @param float $time
	 * @param boolean $hideZeroHours - hide the hour figure if it is zero
	 *
	 * @return string
	 */
	public function formatDuration($time, $hideZeroHours = true, $hideSeconds = false) {
		$hours = $this->toHours($time);
		$minutes = $this->toMinutes($time);
		$seconds = $this->toSeconds($time);
		$formattedTime = $this->padNumber($minutes);
		if(!$hideSeconds) {
			$formattedTime .= ':'.$this->padNumber($seconds);
		}
		if($hours > 0 || !$hideZeroHours) {
			$formattedTime = $hours.':'.$formattedTime;
		}
		return $formattedTime;
	}

	/**
	 * toDecimalPlaces()
	 * convert a value to minutes
	 *
	 * @param float $time
	 * @param int $decimalPlaces optional - set the number of decimal places (default is 2), use to improve granularity
	 *
	 * @return string
	 */    
	public function toTwoDecimalPlaces($number, $decimalPlaces = 2) {
		return number_format((float) $number, $decimalPlaces, '.', ',');
	}

	/**
	 * calculatePace()
	 * calculate the average pace of an activity
	 *
	 * @param int $duration
	 * @param int $distance
	 * @param boolean $toMiles optional - the default output is time per kilometer, set to true for time per mile
	 *
	 * @return float (time)
	 */
	public function calculatePace($duration, $distance, $toMiles = false) {
		if($toMiles) {
			$distance = $this->toMiles($distance);
		}
		$pace = $duration / $distance;
		return $this->formatDuration($pace);
	}

}