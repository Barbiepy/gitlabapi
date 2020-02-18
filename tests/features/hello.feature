Scenario Outline: user got a message to console
    Given user pass a <message> to argument
    Then user see a <message> in console

    Examples:
    | message              |
    | Hello world!         |
    | My name is Python    |
