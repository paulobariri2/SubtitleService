# Subtitle Service

Service to search and download subtitles in `legendas.tv` site.

## Usage

Before start rename `config.ini.example`file to `config.ini` and populate with appropriate values.

Create below environment variables.

- `USERNAME=<legendas.tv login name>`
- `PASSWORD=<legendas.tv password>`

Create below environment variables if proxy is needed.

- `PROXY_HTTP=<http proxy>`
- `PROXY_HTTPS=<https proxy>`

### Search for titles

**Definition**

`GET /titles/{search string}`

**Response**

- `200 OK` on success

```json
[
  {
    "image": "http://i.legendas.tv/poster/214x317/60/4f/tt412142.jpg",
    "id": "25402",
    "span": "House M.D.",
    "text": "House M.D. - 8ª Temporada"
  },
  {
    "image": "http://i.legendas.tv/poster/214x317/7c/4c/legendas_tv_20150818181122.jpg",
    "id": "38680",
    "span": "Full House",
    "text": "Três é Demais - 8ª Temporada"
  }
]
```

### Retrieve title's subtitles

**Definition**

`GET /subtitles/{title id}`

Title id can be obtained from previous API.

**Response**

- `200 OK` on success

```json
[
  {
    "number": "1",
    "class": "destaque",
    "url": "/download/5e60696909678/Law_Order_Special_Victims_Unit/Law_and_Order_SVU_S21E16_HDTV_x264_SVA_AVS_AFG_AMRAP_METCON_ION10_PSA_NTb",
    "name": "Law.and.Order.SVU.S21E16.HDTV.x264-SVA-AVS-AFG-AMRAP-METCON-ION10-PSA-NTb",
    "id": "5e60696909678",
    "data": "1051 downloads, nota 10, enviado por QueensOfTheLab em 04/03/2020 - 23:52 ",
    "uploader": "QueensOfTheLab"
  },
  {
    "number": "2",
    "class": "",
    "url": "/download/5e54998146734/Law_Order_Special_Victims_Unit/Law_and_Order_SVU_S21E15_HDTV_x264_SVA_AVS_AFG_AMRAP_METCON_ION10_PSA_NTb",
    "name": "Law.and.Order.SVU.S21E15.HDTV.x264-SVA-AVS-AFG-AMRAP-METCON-ION10-PSA-NTb",
    "id": "5e54998146734",
    "data": "1213 downloads, nota 10, enviado por QueensOfTheLab em 25/02/2020 - 00:50 ",
    "uploader": "QueensOfTheLab"
  }
]
```

### Download subtitle

**Definition**

`POST /download`

**Arguments**

- `subtitleId:string` can be obtained from previous API
- `outputName:string` name that will be used to save downloaded ZIP file

ZIP file will be saved in current workspace directory.

**Response**

`201 CREATED` on success

```json
{
    "fileName": "This.Is.Us.S04E14.HDTV.x264-KILLERS-AFG-ION10-KiNGS.zip",
    "fileLocation": "/usr/src/app",
    "subtitleId": "5e53bc8eac7e3",
    "subtitles": [
        "legendas_tv_20200224120747878/This.Is.Us.S04E14.720p.HDTV.x264-KILLERS.srt",
        "legendas_tv_20200224120747878/This.Is.Us.S04E14.HDTV.x264-KILLERS.srt",
        "legendas_tv_20200224120747878/This.Is.Us.S04E14.The.Cabin.1080p.AMZN.WEB-DL.DDP5.1.H.264-KiNGS.srt",
        "legendas_tv_20200224120747878/This.Is.Us.S04E14.The.Cabin.720p.AMZN.WEB-DL.DDP5.1.H.264-KiNGS.srt",
        "legendas_tv_20200224120747878/This.Is.Us.S04E14.WEBRip.x264-ION10.srt",
        "legendas_tv_20200224120747878/This.Is.Us.S04E14.XviD-AFG.srt"
    ]
}
```
