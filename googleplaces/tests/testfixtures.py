"""
Sample JSON responses pulled from Google Places API.
"""

PLACES_QUERY_RESPONSE = {
   "html_attributions" : [
      "Listings by \u003ca href=\"http://www.yellowpages.com.au/\"\u003eYellow Pages\u003c/a\u003e"
   ],
   "results" : [
      {
         "geometry" : {
            "location" : {
               "lat" : -33.8719830,
               "lng" : 151.1990860
            }
         },
         "icon" : "http://maps.gstatic.com/mapfiles/place_api/icons/restaurant-71.png",
         "id" : "677679492a58049a7eae079e0890897eb953d79b",
         "name" : "Zaaffran Restaurant - BBQ and GRILL, Darling Harbour",
         "rating" : 3.90,
         "reference" : "CpQBjAAAAFAOaZhKjoDYfDsnISY6p4DKgdtrXTLJBhYsF0WnLBrkLHN3LdLpxc9VsbQKfbtg87nnDsl-SdCKT60Vs4Sxe_lCNCgRBxgq0JBBj8maNZ9pEp_LWjq8O-shdjh-LexdN5o-ZYLVBXhqX2az4TFvuOqme0eRirqMyatKgfn9nuKEkKR2a5tfFQlMfSZSlbyoOxIQVffhpcBqaua-_Yb364wx9xoUC1I-81Wj7aBmSmkctXv_YE7jqgQ",
         "place_id": "ChIJfZmx2Jxw44kR11GqlDbYxxx",
         "types" : [ "restaurant", "food", "establishment" ],
         "vicinity" : "Harbourside Centre 10 Darling Drive, Darling Harbour, Sydney"
      },
      {
         "geometry" : {
            "location" : {
               "lat" : -33.8721970,
               "lng" : 151.1987820
            }
         },
         "icon" : "http://maps.gstatic.com/mapfiles/place_api/icons/restaurant-71.png",
         "id" : "27ea39c8fed1c0437069066b8dccf958a2d06f19",
         "name" : "Criniti's",
         "rating" : 3.10,
         "reference" : "CmRgAAAAm4ajUz0FWaV2gB5mBbdIFhg-Jn98p1AQOrr1QxUWh7Q0nhEUhZL-hY9L4l5ifvRfGttf_gyBpSsGaxMjnr_pcPGUIQKES0vScLQpwM7jsS3BQKB83G9B_SlJFcRuD5dDEhCoNxepsgfJ5YSuXlYjVo9tGhQaKigmZ0WQul__A702AiH3WIy6-A",
         "place_id": "ChIJfZmx2Jxw44kR11GqlDbYsss",
         "types" : [ "restaurant", "food", "establishment" ],
         "vicinity" : "231/10 Darling Dr, DARLING HARBOUR"
      },
      {
         "geometry" : {
            "location" : {
               "lat" : -33.8720340,
               "lng" : 151.198540
            }
         },
         "icon" : "http://maps.gstatic.com/mapfiles/place_api/icons/restaurant-71.png",
         "id" : "cb853832ab8368db3adc52c657fe063dac0f3b11",
         "name" : "Al Ponte Harbour View Restaurant",
         "reference" : "CoQBeAAAAMQ4yYBquhcHj8qzcgUNdwgeiIOhh-Eyf21y9J58y9JXVO7yzw1mFd_wKKjEYJLR_PPjbPRGJEDFnR6eCK_zw1qwrzdyxjnM2zwvdiJ-MLwt3PxVvkkPAjLJYp1cerBc0KTyUVfBo7B4U7RFt4r3DueQ4mz6N-6G7CBoddtfRnm5EhCSGc8yi1k4EQ8whHhKfzxpGhTA1mKVV8kydhqLCsbWDitFMxqzvA",
         "place_id": "ChIJfZmx2Jxw44kR11GqlDbYyyy",
         "types" : [ "restaurant", "food", "establishment" ],
         "vicinity" : "10 Darling Dr, Sydney CBD"
      },
      {
         "geometry" : {
            "location" : {
               "lat" : -33.8711490,
               "lng" : 151.1985180
            }
         },
         "icon" : "http://maps.gstatic.com/mapfiles/place_api/icons/restaurant-71.png",
         "id" : "400d8b4ee30d39175f69fddfcc50590860e59d62",
         "name" : "JB's Bar at Holiday Inn Darling Harbour",
         "reference" : "CoQBfgAAACn9RQ5w_BCAcdF14KQjTh_youPZUA5a7Fbbc74gu3gWaGkl78jlDnIYuUCNOEBs4Up-iw_KrHHDRx58A91Pwqnhrf5RSMihz5gAj3M7X7IW8a_Qxl7-MuAbkoNd6rTbHXtTTWtFtKAhQBljsHPahn0kDPXXSwrhn3WjSfFQX6FfEhCWPSB0ISfYioqpCBWFveZlGhSdW7eYv0NUEAtgTAzJ7x0r4NDHPQ",
         "place_id": "ChIJfZmx2Jxw44kR11GqlDbYzzz",
         "types" : [ "restaurant", "food", "establishment" ],
         "vicinity" : "Furama Hotel, 68 Harbour Street, Darling Harbour, Sydney"
      },
      {
         "geometry" : {
            "location" : {
               "lat" : -33.8711490,
               "lng" : 151.1985180
            }
         },
         "icon" : "http://maps.gstatic.com/mapfiles/place_api/icons/generic_business-71.png",
         "id" : "f12a10b450db59528c18e57dea9f56f88c65c2fa",
         "name" : "Health Harbour",
         "reference" : "CnRlAAAA97YiSpT9ArwBWRZ_7FeddhMtQ4rGTy9v277_B4Y3jxUFKkZVczf3YHrhSLGuKugNQQpCDMWjYKv6LkSA8CiECzh5z7B2wOMkhn0PGjpq01p0QRapJuA6z9pQFS_oTeUq0M_paSCQ_GEB8A5-PpkJXxIQHAuoj0nyrgNwjLtByDHAgBoUdHaA6D2ceLp8ga5IJqxfqOnOwS4",
         "place_id": "ChIJfZmx2Jxw44kR11GqlDbYmmm",
         "types" : [ "food", "store", "establishment" ],
         "vicinity" : "Darling Harbour"
      }
   ],
   "status" : "OK"
}

AUTOCOMPLETE_QUERY_RESPONSE = {
    'predictions': [
        {
            'description': u"Hattie B's Hot Chicken, 19th Avenue South, Nashville, TN, United States",
            'id': '8d41b3887c71f5240a26d8b5badc792708e5ea2a',
            'matched_substrings': [{'length': 6, 'offset': 0}],
            'place_id': 'ChIJSbQCipNmZIgRm4c6Nz9sGaE',
            'reference': 'CmRWAAAAqGYRANjgide_-pBFmUnaOY-m5Cy0RV8by6-pDkB_FsqouiehU-j-dV6oAdZuoMueEvKAqE1FAXcNivsB0mx9a40EEpPOXKKSiag_8wuFAlwGpeQUoXwn_ccF5zs6vldhEhAm161WaDqwSfBFKqjRE04vGhS3BcwJ2MeUbpuPbtVTUx3w3OEpLQ',
            "place_id": "ChIJfZmx2Jxw44kR11GqlDbYnnn",
            'terms': [
                {'offset': 0, 'value': u"Hattie B's Hot Chicken"},
                {'offset': 24, 'value': '19th Avenue South'},
                {'offset': 43, 'value': 'Nashville'},
                {'offset': 54, 'value': 'TN'},
                {'offset': 58, 'value': 'United States'}
            ],
            'types': ['establishment']
        },
        {
            'description': 'Hattiesburg, MS, United States',
            'id': '25f9c17302a8a1a8e432c53d6d4c712063e93188',
            'matched_substrings': [{'length': 6, 'offset': 0}],
            'place_id': 'ChIJ3yio1UncnIgRyrUcLZK_sXQ',
            'reference': 'CkQ2AAAAwRcCnvJl5ZvhsZ6TxUrkpDqPIW7mVIANGti65-SK7MlCNEPj7vGkN2Dh_KnxI7XI6pyDcTsXCoi7wLnQrr4H7xIQ_D35yzn61ZNmQelYcjk9xBoUsgP8yimN1xd9J4L6k4b6ZpK_E94',
            "place_id": "ChIJfZmx2Jxw44kR11GqlDbYooo",
            'terms': [
                {'offset': 0, 'value': 'Hattiesburg'},
                {'offset': 13, 'value': 'MS'},
                {'offset': 17, 'value': 'United States'}
            ],
            'types': ['locality', 'political', 'geocode']\
        },
        {
            'description': 'Hattie Cotton Elementary School, Nashville, TN, United States',
            'id': 'f8998e62bf80300a07a8d007b890bb17368b3fd4',
            'matched_substrings': [{'length': 6, 'offset': 0}],
            'place_id': 'ChIJXzft89tnZIgRm0ovqWZebMs',
            'reference': 'ClRMAAAAVe4DIy63p4YGFHVQpmlrgBXkA1K0T6xZbWm2SHitS28bZcPl2ctmi7QNKR2EX_2RNY5ckfPVIBL3iDOmhzjeuCrn48qNnoE0z9QJzskfdnASEKo5EvKlKYNuqep4dyThEDcaFFYegROsLxF0tssPzZAYyL9ra70z',
            "place_id": "ChIJfZmx2Jxw44kR11GqlDbYppp",
            'terms': [
                {'offset': 0, 'value': 'Hattie Cotton Elementary School'},
                {'offset': 33, 'value': 'Nashville'},
                {'offset': 44, 'value': 'TN'},
                {'offset': 48, 'value': 'United States'}
            ],
            'types': ['establishment']
        },
        {
            'description': 'Hattie Ct, Hendersonville, TN, United States',
            'id': 'eaeb7403d82be002de3ae52ab811d4014d4dff5b',
            'matched_substrings': [{'length': 6, 'offset': 0}],
            'place_id': 'EixIYXR0aWUgQ3QsIEhlbmRlcnNvbnZpbGxlLCBUTiwgVW5pdGVkIFN0YXRlcw',
            'reference': 'CjQwAAAA16vktOVr7wLMig9H8Eb0CQFaDuIhqsG-3G7YCH7NE9qKxImG9p8W_mXbhjnkg9f4EhA6hP-p7r4I-iBMu6vcpb2VGhRFB4IPb0QupUlhD_B-Q8T6UJ8NQQ',
            "place_id": "ChIJfZmx2Jxw44kR11GqlDbYqqq",
            'terms': [
                {'offset': 0, 'value': 'Hattie Ct'},
                {'offset': 11, 'value': 'Hendersonville'},
                {'offset': 27, 'value': 'TN'},
                {'offset': 31, 'value': 'United States'}
            ],
            'types': ['route', 'geocode']
        },
        {
            'description': 'Hattieville, AR, United States',
            'id': '4a144096d3107fd6f3ef0254c5ca4dd106abebcd',
            'matched_substrings': [{'length': 6, 'offset': 0}],
            'place_id': 'ChIJjTUp5w2izYcRwRTy8ZpwjkI',
            'reference': 'CkQ2AAAA-9G9z7Y3SSTPJOxNcCSVhUxeaC7OTL_ADLq00_WXSHBhXi1PTsm08gX2Zz_uLnLTBFJhqxm4g9HrbTO8Rm25lBIQepnjuQ02A6BqH2lNVjsIzRoUM_ndW4AhrGZFxnKOWSAPWfAm7hY',
            "place_id": "ChIJfZmx2Jxw44kR11GqlDbYrrr",
            'terms': [
                {'offset': 0, 'value': 'Hattieville'},
                {'offset': 13, 'value': 'AR'},
                {'offset': 17, 'value': 'United States'}
            ],
            'types': ['locality', 'political', 'geocode']
        }
    ],
    'status': 'OK'
}