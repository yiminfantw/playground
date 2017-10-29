<?php

class MyLdapContactsSuggestionsPlugin extends \RainLoop\Plugins\AbstractPlugin
{
	public function Init()
	{
		$this->addHook('main.fabrica', 'MainFabrica');
	}

	/**
	 * @param string $sName
	 * @param mixed $mResult
	 */
	public function MainFabrica($sName, &$mResult)
	{
		switch ($sName)
		{
			case 'suggestions':

				if (!\is_array($mResult))
				{
					$mResult = array();
				}

				include_once __DIR__.'/MyLdapContactsSuggestions.php';
				$mResult[] = new MyLdapContactsSuggestions();
				break;
		}
	}
}
