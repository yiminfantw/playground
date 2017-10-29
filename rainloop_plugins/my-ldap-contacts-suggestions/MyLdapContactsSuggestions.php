<?php

class MyLdapContactsSuggestions implements \RainLoop\Providers\Suggestions\ISuggestions
{
	/**
	 * @param \RainLoop\Model\Account $oAccount
	 * @param string $sQuery
	 * @param int $iLimit = 20
	 *
	 * @return array
	 */
	public function Process($oAccount, $sQuery, $iLimit = 20)
	{
                /*
		* $aResult = array(
		* 	 array($oAccount->Email(), ''),
		*   	 array('email@domain.com', 'name')
		*);
                */
                $sContactManager = dirname(__FILE__) . '/contact_manager.py';
                $sToken = '<TOKEN>';
                $sDomain = '<DOMAIN>';
                $aResult = json_decode(exec('python ' . $sContactManager . ' -src ldap -fmt rainloop -tk ' . $sToken . ' -dm ' . $sDomain . ' -sc ' . $sQuery), true);

		return $aResult;
	}
}
