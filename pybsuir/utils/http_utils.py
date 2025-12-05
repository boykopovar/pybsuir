from typing import Union, Optional, BinaryIO

from pybsuir.exceptions.exceptions_utils import create_api_exception

TIMEOUT: int = 60

try:
    import aiohttp

    class _Client:
        @staticmethod
        async def request(method, url, *, headers, ok_status, timeout, payload=None, params=None, session=None):
            timeout = timeout or TIMEOUT

            async def fetch(sess):
                async with getattr(sess, method)(url, headers=headers, json=payload, params=params, timeout=timeout) as r:
                    if r.status not in (ok_status if isinstance(ok_status, list) else [ok_status]):
                        raise create_api_exception(r.status, url, await r.text(), dict(r.headers))
                    if r.content_length == 0 or not r.headers.get("Content-Type", "").startswith("application/json"):
                        return {}
                    return await r.json()

            if session:
                return await fetch(session)
            async with aiohttp.ClientSession() as session:
                return await fetch(session)

        @staticmethod
        async def post_no_redirect(url, headers, ok_status: Union[int, list], timeout, payload=None, session=None):
            timeout = timeout or TIMEOUT

            async def fetch(sess):
                async with sess.post(url, headers=headers, json=payload, timeout=timeout, allow_redirects=False) as r:
                    if r.status not in (ok_status if isinstance(ok_status, list) else [ok_status]):
                        raise create_api_exception(r.status, url, await r.text(), dict(r.headers))
                    return r.status, dict(r.headers), await r.text()

            if session:
                return await fetch(session)
            async with aiohttp.ClientSession() as session:
                return await fetch(session)

        @staticmethod
        async def get_no_json(url, headers, ok_status: Union[int, list], timeout, params=None, session=None):
            timeout = timeout or TIMEOUT

            async def fetch(sess):
                async with sess.get(url, headers=headers, params=params, timeout=timeout) as r:
                    if r.status not in (ok_status if isinstance(ok_status, list) else [ok_status]):
                        raise create_api_exception(r.status, url, await r.text(), dict(r.headers))
                    return r.status, dict(r.headers), await r.text()

            if session:
                return await fetch(session)
            async with aiohttp.ClientSession() as session:
                return await fetch(session)

        @staticmethod
        async def post_no_json(url, headers, ok_status: Union[int, list], timeout, payload=None, session=None):
            timeout = timeout or TIMEOUT

            async def fetch(sess):
                async with sess.post(url, headers=headers, json=payload, timeout=timeout) as r:
                    if r.status not in (ok_status if isinstance(ok_status, list) else [ok_status]):
                        raise create_api_exception(r.status, url, await r.text(), dict(r.headers))
                    return r.status, dict(r.headers), await r.text()

            if session:
                return await fetch(session)
            async with aiohttp.ClientSession() as session:
                return await fetch(session)

        @staticmethod
        def create_session():
            return aiohttp.ClientSession()

        @staticmethod
        async def close_session(session):
            await session.close()

        @staticmethod
        async def upload_to_gcs(session: aiohttp.ClientSession,
                                file_data: BinaryIO,
                                gcs_data: dict,
                                ride_id: str,
                                timeout: int) -> None:
            url = gcs_data["url"]
            fields = gcs_data["fields"]
            data = aiohttp.FormData()
            for k, v in fields.items():
                data.add_field(k, str(v))
            file_data.seek(0)
            data.add_field("file", file_data, filename=fields["key"].split("/")[-1])
            async with session.post(url, data=data, timeout=timeout) as r:
                if r.status != 204:
                    raise create_api_exception(r.status, url, await r.text(), dict(r.headers), ride_id)

except ImportError:
    try:
        import httpx

        class _Client:
            @staticmethod
            async def request(method, url, *, headers, ok_status, timeout, payload=None, params=None, session=None):
                timeout = timeout or TIMEOUT

                async def fetch(sess):
                    r = await sess.request(method, url, headers=headers, json=payload, params=params, timeout=timeout)
                    if r.status_code not in (ok_status if isinstance(ok_status, list) else [ok_status]):
                        raise create_api_exception(r.status_code, url, r.text, dict(r.headers))
                    if r.headers.get("Content-Length") == "0" or not r.headers.get("Content-Type", "").startswith("application/json"):
                        return {}
                    return r.json()

                if session:
                    return await fetch(session)
                async with httpx.AsyncClient() as session:
                    return await fetch(session)

            @staticmethod
            async def post_no_redirect(url, headers, ok_status: Union[int, list], timeout, payload=None, session=None):
                timeout = timeout or TIMEOUT

                async def fetch(sess):
                    r = await sess.request("post", url, headers=headers, json=payload, timeout=timeout, allow_redirects=False)
                    if r.status_code not in (ok_status if isinstance(ok_status, list) else [ok_status]):
                        raise create_api_exception(r.status_code, url, r.text, dict(r.headers))
                    return r.status_code, dict(r.headers), r.text

                if session:
                    return await fetch(session)
                async with httpx.AsyncClient() as session:
                    return await fetch(session)

            @staticmethod
            async def get_no_json(url, headers, ok_status: Union[int, list], timeout, params=None, session=None):
                timeout = timeout or TIMEOUT

                async def fetch(sess):
                    r = await sess.request("get", url, headers=headers, params=params, timeout=timeout)
                    if r.status_code not in (ok_status if isinstance(ok_status, list) else [ok_status]):
                        raise create_api_exception(r.status_code, url, r.text, dict(r.headers))
                    return r.status_code, dict(r.headers), r.text

                if session:
                    return await fetch(session)
                async with httpx.AsyncClient() as session:
                    return await fetch(session)

            @staticmethod
            async def post_no_json(url, headers, ok_status: Union[int, list], timeout, payload=None, session=None):
                timeout = timeout or TIMEOUT

                async def fetch(sess):
                    r = await sess.request("post", url, headers=headers, json=payload, timeout=timeout)
                    if r.status_code not in (ok_status if isinstance(ok_status, list) else [ok_status]):
                        raise create_api_exception(r.status_code, url, r.text, dict(r.headers))
                    return r.status_code, dict(r.headers), r.text

                if session:
                    return await fetch(session)
                async with httpx.AsyncClient() as session:
                    return await fetch(session)

            @staticmethod
            def create_session():
                return httpx.AsyncClient()

            @staticmethod
            async def close_session(session):
                await session.aclose()

            @staticmethod
            async def upload_to_gcs(*args, **kwargs):
                raise NotImplementedError("upload_to_gcs requires aiohttp")

    except ImportError:
        from urllib.request import Request, urlopen
        from urllib.parse import urlencode
        import json
        import contextvars
        import functools
        from asyncio import events
        import gzip
        import zlib

        async def _to_thread(func, /, *args, **kwargs):
            loop = events.get_running_loop()
            ctx = contextvars.copy_context()
            func_call = functools.partial(ctx.run, func, *args, **kwargs)
            return await loop.run_in_executor(None, func_call)

        class _Client:
            @staticmethod
            async def request(method, url, *, headers, ok_status, timeout, payload=None, params=None, session=None):
                timeout = timeout or TIMEOUT

                if params:
                    url += '?' + urlencode(params)
                if payload:
                    payload = json.dumps(payload).encode('utf-8')
                    headers['Content-Type'] = 'application/json'
                req = Request(url, data=payload, headers=headers, method=method.upper())

                def fetch():
                    try:
                        with urlopen(req, timeout=timeout) as r:
                            content_encoding = r.getheader('Content-Encoding')
                            data = r.read()
                            if content_encoding == 'gzip':
                                data = gzip.decompress(data)
                            elif content_encoding == 'deflate':
                                data = zlib.decompress(data)
                            status = r.getcode()
                            headers_resp = dict(r.getheaders())
                            if status not in (ok_status if isinstance(ok_status, list) else [ok_status]):
                                raise create_api_exception(status, url, data.decode('utf-8'), headers_resp)
                            if r.getheader('Content-Length') ==0 or not r.getheader('Content-Type', '').startswith('application/json'):
                                return {}
                            return json.loads(data)
                    except Exception as e:
                        raise create_api_exception(getattr(e, 'code', 500), url, str(e), {})

                return await _to_thread(fetch)

            @staticmethod
            async def post_no_redirect(url, headers, ok_status: Union[int, list], timeout, payload=None, session=None):
                timeout = timeout or TIMEOUT

                def fetch():
                    try:
                        data = json.dumps(payload).encode("utf-8")
                        headers["Content-Type"] = "application/json"
                        req = Request(url, data=data, headers=headers, method="POST")
                        with urlopen(req, timeout=timeout) as r:
                            status = r.getcode()
                            headers_resp = dict(r.getheaders())
                            text = r.read().decode("utf-8")
                            if status not in (ok_status if isinstance(ok_status, list) else [ok_status]):
                                raise create_api_exception(status, url, text, headers_resp)
                            return status, headers_resp, text
                    except Exception as e:
                        raise create_api_exception(getattr(e, 'code', 500), url, str(e), {})

                return await _to_thread(fetch)

            @staticmethod
            async def get_no_json(url, headers, ok_status: Union[int, list], timeout, params=None, session=None):
                timeout = timeout or TIMEOUT

                if params:
                    url += '?' + urlencode(params)
                req = Request(url, headers=headers, method="GET")

                def fetch():
                    try:
                        with urlopen(req, timeout=timeout) as r:
                            content_encoding = r.getheader('Content-Encoding')
                            data = r.read()
                            if content_encoding == 'gzip':
                                data = gzip.decompress(data)
                            elif content_encoding == 'deflate':
                                data = zlib.decompress(data)
                            status = r.getcode()
                            headers_resp = dict(r.getheaders())
                            if status not in (ok_status if isinstance(ok_status, list) else [ok_status]):
                                raise create_api_exception(status, url, data.decode('utf-8'), headers_resp)
                            return status, headers_resp, data.decode('utf-8')
                    except Exception as e:
                        raise create_api_exception(getattr(e, 'code', 500), url, str(e), {})

                return await _to_thread(fetch)

            @staticmethod
            async def post_no_json(url, headers, ok_status: Union[int, list], timeout, payload=None, session=None):
                timeout = timeout or TIMEOUT

                if payload:
                    payload = json.dumps(payload).encode('utf-8')
                    headers['Content-Type'] = 'application/json'
                req = Request(url, data=payload, headers=headers, method="POST")

                def fetch():
                    try:
                        with urlopen(req, timeout=timeout) as r:
                            content_encoding = r.getheader('Content-Encoding')
                            data = r.read()
                            if content_encoding == 'gzip':
                                data = gzip.decompress(data)
                            elif content_encoding == 'deflate':
                                data = zlib.decompress(data)
                            status = r.getcode()
                            headers_resp = dict(r.getheaders())
                            if status not in (ok_status if isinstance(ok_status, list) else [ok_status]):
                                raise create_api_exception(status, url, data.decode('utf-8'), headers_resp)
                            return status, headers_resp, data.decode('utf-8')
                    except Exception as e:
                        raise create_api_exception(getattr(e, 'code', 500), url, str(e), {})

                return await _to_thread(fetch)

            @staticmethod
            def create_session():
                return None

            @staticmethod
            async def close_session(session):
                pass

            @staticmethod
            async def upload_to_gcs(*args, **kwargs):
                raise NotImplementedError("upload_to_gcs requires aiohttp")

async def get_json_response(url, headers, ok_status: Union[int, list], timeout, params=None, session: Optional[object] = None) -> dict:
    return await _Client.request("get", url, headers=headers, ok_status=ok_status, timeout=timeout, params=params, session=session)

async def post_json_response(url, headers, ok_status: Union[int, list], timeout, payload=None, session: Optional[object] = None) -> dict:
    return await _Client.request("post", url, headers=headers, ok_status=ok_status, timeout=timeout, payload=payload, session=session)

async def patch_json_response(url, headers, payload, ok_status: Union[int, list], timeout, session: Optional[object] = None) -> dict:
    return await _Client.request("patch", url, headers=headers, ok_status=ok_status, timeout=timeout, payload=payload, session=session)

async def delete_json_response(url, headers, ok_status: Union[int, list], timeout, payload=None, session: Optional[object] = None) -> dict:
    return await _Client.request("delete", url, headers=headers, ok_status=ok_status, timeout=timeout, payload=payload, session=session)

async def post_json_no_redirect(url, headers, ok_status: Union[int, list], timeout, payload=None, session=None):
    return await _Client.post_no_redirect(url, headers=headers, ok_status=ok_status, timeout=timeout, payload=payload, session=session)

async def get_http(url, headers, ok_status: Union[int, list], timeout, params=None, session=None):
    return await _Client.get_no_json(url, headers=headers, ok_status=ok_status, timeout=timeout, params=params, session=session)

async def post_http(url, headers, ok_status: Union[int, list], timeout, payload=None, session=None):
    return await _Client.post_no_json(url, headers=headers, ok_status=ok_status, timeout=timeout, payload=payload, session=session)

def create_async_session():
    return _Client.create_session()

async def close_async_session(session):
    await _Client.close_session(session)

async def upload_to_gcs(session, file_data, gcs_data, ride_id, timeout):
    await _Client.upload_to_gcs(session, file_data, gcs_data, ride_id, timeout)