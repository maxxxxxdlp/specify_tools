<?php

//SET YOUR OWN TOKEN AND USERNAME HERE
require_once($_SERVER['DOCUMENT_ROOT'].'/functions/Tokens.php');
$token = Tokens::get('github_token');
$github_username = Tokens::get('github_username');

?>

<!DOCTYPE html>
<html lang="en">

	<head>

		<meta charset="utf-8">
		<title>Specify Release Log</title>
		<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha256-L/W5Wfqfa0sdBNIKN9cG6QA5F2qx4qICmU2VgLruv9Y=" crossorigin="anonymous" />
		<link rel="icon" href="https://www.sustain.specifysoftware.org/wp-content/uploads/2017/03/toolbar_id.png" sizes="32x32">
		<link rel="icon" href="https://www.sustain.specifysoftware.org/wp-content/uploads/2017/03/toolbar_id.png" sizes="192x192">
		<link rel="apple-touch-icon-precomposed" href="https://www.sustain.specifysoftware.org/wp-content/uploads/2017/03/toolbar_id.png">

	</head>

	<body class="container-fluid"><br> <?php

		//REPOS
		$current_repo = $_GET['repository'];

		$cURLConnection = curl_init('https://api.github.com/orgs/specify/repos?sort=updated');
		curl_setopt($cURLConnection, CURLOPT_HTTPHEADER, [
			'User-Agent: '.$github_username,
		]);
		curl_setopt($cURLConnection, CURLOPT_USERPWD, $github_username.':'.$token);
		curl_setopt($cURLConnection, CURLOPT_RETURNTRANSFER, true);

		$apiResponse = curl_exec($cURLConnection);
		curl_close($cURLConnection);

		$jsonArrayResponse = json_decode($apiResponse);

		$repos_array = [];
		foreach($jsonArrayResponse as $repo)
			$repos_array[] = $repo->name;


		echo '<form>

			<label class="form-group">

				Repository: <br>

				<select class="form-control" name="repository">';

					foreach($repos_array as $repo){

						$selected = '';
						if($current_repo==$repo)
							$selected = 'selected';

						echo '<option value="'.$repo.'" '.$selected.'>'.$repo.'</option>';

					}

				echo '</select>

			</label><br><br>

			<input type="submit" value="Select Repository" class="btn btn-primary"><br><br>

		</form>';

		if($_GET['repository']=='')
			exit();



		//MILESTONES
		$milestone_name = $_GET['milestone'];
		$milestone_value = '';
		$milestone_selected = $milestone_name!=NULL;

		if( $milestone_name == '*' || $milestone_name == '' || $milestone_name == null)
			$milestone_value = '*';
		elseif($milestone_name == 'none')
			$milestone_value = 'none';

		$cURLConnection = curl_init('https://api.github.com/repos/specify/'.$current_repo.'/milestones');
		curl_setopt($cURLConnection, CURLOPT_HTTPHEADER, [
			'User-Agent: maxxxxxdlp',
		]);
		curl_setopt($cURLConnection, CURLOPT_USERPWD, 'maxxxxxdlp:'.$token);
		curl_setopt($cURLConnection, CURLOPT_RETURNTRANSFER, true);

		$apiResponse = curl_exec($cURLConnection);
		curl_close($cURLConnection);

		$jsonArrayResponse = json_decode($apiResponse);

		$milestones_array = [];
		$milestone_number = false;
		foreach($jsonArrayResponse as $milestone){

			if($milestone_value == '' && $milestone->number == $milestone_name)
				$milestone_number = $milestone->number;

			$milestones_array[] = [$milestone->number,$milestone->title,strtotime($milestone->updated_at)];

		}

		if($milestone_value==''){

			if($milestone_number === false)
				exit('Milestone not found');

			$milestone_value = $milestone_number;

		}

		function compare_milestones($a, $b){
			if($a[2] == $b[2])
				return 0;
			elseif ($a[2] > $b[2])
				return -1;
			else
				return 1;
		}
		usort($milestones_array, 'compare_milestones');
		if(!$milestone_selected && count($milestones_array)>0)
			$milestone_value = $milestones_array[0][0];



		//LABELS
		$labels_selected = $_GET['labels'];

		$cURLConnection = curl_init('https://api.github.com/repos/specify/'.$current_repo.'/labels');
		curl_setopt($cURLConnection, CURLOPT_HTTPHEADER, [
			'User-Agent: maxxxxxdlp',
		]);
		curl_setopt($cURLConnection, CURLOPT_USERPWD, 'maxxxxxdlp:'.$token);
		curl_setopt($cURLConnection, CURLOPT_RETURNTRANSFER, true);

		$apiResponse = curl_exec($cURLConnection);
		curl_close($cURLConnection);

		$jsonArrayResponse = json_decode($apiResponse);

		$labels_array = [];

		foreach($jsonArrayResponse as $label){

			$selected = in_array($label->name,$labels_selected);
			$labels_array[] = [$label->name,$selected];

		}



		//PARAMS STRING
		$params = '';

		if($milestone_value=='none')
			$params.='milestone=&';
		elseif($milestone_value!='*')
			$params.='milestone='.$milestone_value.'&';

		if($labels_selected != [])
			$params .= 'labels='.implode(',',$labels_selected).'&';



		//ISSUES

		$count = 0;

		function get_issues($page = 1){

			global $count, $params, $token, $current_repo;

			$cURLConnection = curl_init('https://api.github.com/repos/specify/'.$current_repo.'/issues?' . $params . 'page=' . $page);
			curl_setopt($cURLConnection, CURLOPT_HTTPHEADER, [
				'User-Agent: maxxxxxdlp',
			]);
			curl_setopt($cURLConnection, CURLOPT_USERPWD, 'maxxxxxdlp:'.$token);
			curl_setopt($cURLConnection, CURLOPT_RETURNTRANSFER, 1);
			$apiResponse = curl_exec($cURLConnection);
			curl_close($cURLConnection);

			$jsonArrayResponse = json_decode($apiResponse);
			$count += count($jsonArrayResponse);

			if($jsonArrayResponse==[])
				return false;

			$result = '';

			foreach($jsonArrayResponse as $issue){
				$url = $issue->url;
				$url = str_replace('api.', '', $url);
				$url = str_replace('repos/', '', $url);

				$result .= '<a target="_blank" href="'.$url . '">#' . $issue->number . '</a> ' . $issue->title . '<br>';
			}

			$next_result = get_issues($page + 1);
			if($next_result != false)
				$result .= $next_result;

			return $result;
		}

		$content = get_issues();

		$milestone_all_selected = '';
		$milestone_none_selected = '';

		if($milestone_value == '*')
			$milestone_all_selected = ' selected';
		elseif($milestone_value == 'none')
			$milestone_none_selected = ' selected'; ?>

		<form>

			<input type="hidden" name="repository" value="<?=$current_repo?>">

			<label class="form-group">Milestone:<br>
				<select class="form-control" name="milestone">

					<option value="*"<?=$milestone_all_selected?>>All</option>
					<option value="none"<?=$milestone_none_selected?>>Issues with no milestone</option> <?php

					foreach($milestones_array as $milestone){

						echo '<option value="' . $milestone[0].'"';

						if($milestone[0] == $milestone_value)
							echo ' selected';

						echo '>'.$milestone[1].'</option>';

					} ?>

				</select>
			</label class="form-group"><br><br>

			<label class="form-group">Labels:<br>
				<select class="form-control" name="labels[]" multiple size="8"><?php

					foreach($labels_array as $label){

						echo '<option value="' . $label[0].'"';

						if($label[1])
							echo ' selected';

						echo '>'.$label[0].'</option>';

					} ?>

				</select>
			</label class="form-group"><br><br>

			<input type="submit" value="Show issues" class="btn btn-success">

		</form><br>

		<p>Total issues: <?=$count?></p>

		<?=$content?><br>

	</body>

</html>
