# this script will update pages, by replacing a picture





## Getting Started

    Phase 1- Install the script
    Phase 2- Run the script

## Prerequisites

  none


## Phase 1:  Install the script

    1- yum install git ( and python3, )
    2- cd ~/Documents ( on windows )
    3- git clone https://github.com/dahai0013/confluence.git ( will be automated in terraform in the future )
    4- mv confluence/credential.yaml.template confluence/credential.yaml
    5- vi confluence/credential.yaml ( an copy your credential to this file )



## Phase 2

    1- python3 search_and_update.py
    2-
    3-

    
            start
            stage1
            stage2
            Before:  <p><a href="http://freetelecomuni.co.uk"><ac:image><ri:url ri:value="http://www.freetelecomuni.co.uk/juniper/lib/header1.jpg" /></ac:image></a></p><p><br /></p><p><a href="https://archive.org/details/librivoxaudio">https://archive.org/details/librivoxaudio</a></p><p><br /></p><p><br /></p>
            dict:
             {"version": {"number": 2}, "title": "Audio Book and other", "type": "page", "body": {"storage": {"value": "<p><ac:image><ri:attachment ri:filename=\"headerFTU.jpg\" ri:version-at-save=\"2\">\"</ac:image></a></p><p><br /></p><p><a href=\"https://archive.org/details/librivoxaudio\">https://archive.org/details/librivoxaudio</a></p><p><br /></p><p><br /></p>"}}}
            {
                "data": {
                    "authorized": false,
                    "errors": [],
                    "successful": false,
                    "valid": true
                },
                "message": "com.atlassian.confluence.api.service.exceptions.ServiceException: java.lang.UnsupportedOperationException: Cannot convert from null to storage",
                "statusCode": 500
            }
            After:  {'version': {'number': 2}, 'title': 'Audio Book and other', 'type': 'page', 'body': {'storage': {'value': '<p><ac:image><ri:attachment ri:filename="headerFTU.jpg" ri:version-at-save="2">"</ac:image></a></p><p><br /></p><p><a href="https://archive.org/details/librivoxaudio">https://archive.org/details/librivoxaudio</a></p><p><br /></p><p><br /></p>'}}}
            stage3


##  python script manual information:

converthtml2confluence.py --help

    usage:  converthtml2confluence.py   <folder name of html and jpg or png>

    Options:
    folder name      Mandatory.

    -option1         ....
    -option2         ....



## Contributing

Everyone is welcome ;-)


## Versioning

Beta version

## Authors

* Me, Myself and I ( https://www.youtube.com/watch?v=P8-9mY-JACM )


## License

Free Code Forever and Wakanda.

## Acknowledgments

* Python Team and Linus Torvalds
* Youtuber, Blogger and contributor of all type
* and You
