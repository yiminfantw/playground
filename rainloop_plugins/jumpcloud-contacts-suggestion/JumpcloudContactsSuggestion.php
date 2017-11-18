<?php

class JumpcloudContactsSuggestion implements \RainLoop\Providers\Suggestions\ISuggestions
{
	private $sApiToken = '';
	private $sEmailDomain = '';

	public function Process($oAccount, $sQuery, $iLimit = 20)
	{
                $sContactManager = dirname(__FILE__) . '/contact_manager.py';
                $aResult = json_decode(
			exec(
				'python ' . $sContactManager . ' -src ldap -fmt rainloop -tk ' . $this->sApiToken . ' -dm ' . $this->sEmailDomain . ' -sc ' . $sQuery
			),
			true
		);

		return $aResult;
	}

	public function SetConfig($sApiToken, $sEmailDomain)
	{
		$this->sApiToken = $sApiToken;
		$this->sEmailDomain = $sEmailDomain;

		return $this;
	}
}
