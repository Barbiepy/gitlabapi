Feature: searching Gitlab projects
    User can get list of Gitlab projects
    Which can be found by search substring
    All found results will be saved to database

Scenario Outline: got not empty list of projects
    Given user pass a <substring> to endpoint
    Then server returns next <number> of projects

    Examples:
    | substring            | number |
    | kremlin              | 2      |
    | whitehouse           | 8      |
