<?php

class JumpcloudContactsSuggestionPlugin extends \RainLoop\Plugins\AbstractPlugin
{
	public function Init()
	{
		$this->addHook('main.fabrica', 'Fabrica');
	}

	public function Fabrica($sName, &$mResult)
	{
		switch ($sName)
		{
			case 'suggestions':
				$sApiToken = \trim($this->Config()->Get('plugin', 'api_token', ''));
				$sEmailDomain = \trim($this->Config()->Get('plugin', 'email_domain', ''));

				if (!\is_array($mResult))
				{
					$mResult = array();
				}

				include_once __DIR__.'/JumpcloudContactsSuggestion.php';
				$oProvider = new JumpcloudContactsSuggestion();
				$oProvider->SetConfig($sApiToken, $sEmailDomain);
				$mResult[] = $oProvider;

				break;
		}
	}

	public function ConfigMapping()
	{
		return array(
			\RainLoop\Plugins\Property::NewInstance('api_token')
				->SetLabel('API Token')
				->SetDefaultValue(''),
			\RainLoop\Plugins\Property::NewInstance('email_domain')
				->SetLabel('Email Domain')
				->SetDefaultValue('renovatiopictures.com')
		);
	}
}
