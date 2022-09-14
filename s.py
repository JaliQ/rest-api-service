array =  [
        {
            "id": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
            "url": None,
            "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            "size": 384,
            "type": "FOLDER",
            "date": "2022-02-02T12:00:00Z",
            "children": [
                {
                    "id": "863e1a7a-1304-42ae-943b-179184c077e3",
                    "url": "/file/url1",
                    "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                    "size": 128,
                    "type": "FILE",
                    "date": "2022-02-02T12:00:00Z",
                    "children": None
                },
                {
                    "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
                    "url": "/file/url2",
                    "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                    "size": 256,
                    "type": "FILE",
                    "date": "2022-02-02T12:00:00Z",
                    "children": None
                }
            ]
        },
        {
            "id": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
            "url": None,
            "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            "size": 1600,
            "type": "FOLDER",
            "date": "2022-02-03T15:00:00Z",
            "children": [
                {
                    "id": "98883e8f-0507-482f-bce2-2fb306cf6483",
                    "url": "/file/url3",
                    "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                    "size": 512,
                    "type": "FILE",
                    "date": "2022-02-03T12:00:00Z",
                    "children": None
                },
                {
                    "id": "74b81fda-9cdc-4b63-8927-c978afed5cf4",
                    "url": "/file/url4",
                    "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                    "size": 1024,
                    "type": "FILE",
                    "date": "2022-02-03T12:00:00Z",
                    "children": None
                },
                {
                    "id": "73bc3b36-02d1-4245-ab35-3106c9ee1c65",
                    "url": "/file/url5",
                    "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                    "size": 64,
                    "type": "FILE",
                    "date": "2022-02-03T15:00:00Z",
                    "children": None
                }
            ]
        }
    ]
print(sorted(array, key = lambda x : x["id"]))
