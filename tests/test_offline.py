from unittest import mock

from httpie.status import ExitStatus

from .fixtures import FILE_CONTENT, FILE_PATH_ARG, patharg
from .utils import http


def test_offline():
    r = http(
        '--offline',
        'https://this-should.never-resolve/foo',
    )
    assert 'GET /foo' in r


def test_offline_raw():
    r = http(
        '--offline',
        '--raw',
        'foo bar',
        'https://this-should.never-resolve/foo',
    )
    assert 'POST /foo' in r
    assert 'foo bar' in r


def test_offline_raw_empty_should_use_POST():
    r = http(
        '--offline',
        '--raw',
        '',
        'https://this-should.never-resolve/foo',
    )
    assert 'POST /foo' in r


def test_offline_form():
    r = http(
        '--offline',
        '--form',
        'https://this-should.never-resolve/foo',
        'foo=bar'
    )
    assert 'POST /foo' in r
    assert 'foo=bar' in r


def test_offline_json():
    r = http(
        '--offline',
        'https://this-should.never-resolve/foo',
        'foo=bar'
    )
    assert 'POST /foo' in r
    assert r.json == {'foo': 'bar'}


def test_offline_multipart():
    r = http(
        '--offline',
        '--multipart',
        'https://this-should.never-resolve/foo',
        'foo=bar'
    )
    assert 'POST /foo' in r
    assert 'name="foo"' in r


def test_offline_from_file():
    r = http(
        '--offline',
        'https://this-should.never-resolve/foo',
        f'@{FILE_PATH_ARG}'
    )
    assert 'POST /foo' in r
    assert FILE_CONTENT in r


def test_offline_chunked():
    r = http(
        '--offline',
        '--chunked',
        '--form',
        'https://this-should.never-resolve/foo',
        'hello=world'
    )
    assert 'POST /foo' in r
    assert 'Transfer-Encoding: chunked' in r, r
    assert 'hello=world' in r


def test_offline_download():
    """Absence of response should be handled gracefully with --download"""
    r = http(
        '--offline',
        '--download',
        'https://this-should.never-resolve/foo',
    )
    assert 'GET /foo' in r


def test_offline_from_file_sets_content_type():
    r = http(
        '--offline',
        'https://this-should.never-resolve/foo',
        f'@{FILE_PATH_ARG}'
    )

    assert 'Content-Type: text/plain' in r


def test_offline_explicit_method_with_data():
    r = http(
        '--offline',
        'PUT',
        'https://this-should.never-resolve/foo',
        'foo=bar'
    )

    assert 'PUT /foo' in r
    assert r.json == {'foo': 'bar'}


def test_offline_file_preserves_explicit_content_type():
    r = http(
        '--offline',
        'https://this-should.never-resolve/foo',
        'Content-Type:application/x-custom',
        f'@{FILE_PATH_ARG}'
    )

    assert 'Content-Type: application/x-custom' in r
    assert FILE_CONTENT in r


def test_offline_does_not_send_request():
    with mock.patch(
        'requests.sessions.Session.send',
        side_effect=AssertionError('Offline mode must not send requests'),
    ) as send:
        r = http(
            '--offline',
            'https://this-should.never-resolve/foo',
            'foo=bar'
        )
        send.assert_not_called()

    assert 'POST /foo' in r
    assert r.json == {'foo': 'bar'}


def test_offline_chunked_file_body():
    r = http(
        '--offline',
        '--chunked',
        'https://this-should.never-resolve/foo',
        f'@{FILE_PATH_ARG}'
    )
    assert 'POST /foo' in r
    assert 'Transfer-Encoding: chunked' in r
    assert FILE_CONTENT in r


def test_offline_file_without_extension(tmp_path):
    file_path = tmp_path / 'payload'
    file_path.write_text('{"foo": "bar"}', encoding='utf-8')
    r = http(
        '--offline',
        '--json',
        'https://this-should.never-resolve/foo',
        f'@{patharg(file_path)}'
    )
    assert 'POST /foo' in r
    assert 'Content-Type: application/json' in r
    assert r.json == {'foo': 'bar'}


def test_offline_empty_file_body(tmp_path):
    file_path = tmp_path / 'empty.txt'
    file_path.write_bytes(b'')
    r = http(
        '--offline',
        'https://this-should.never-resolve/foo',
        f'@{patharg(file_path)}'
    )
    assert 'POST /foo' in r
    headers, separator, body = r.partition('\r\n\r\n')
    assert separator
    assert body.strip() == ''


def test_offline_file_field_error_suggests_form():
    with mock.patch(
        'requests.sessions.Session.send',
        side_effect=AssertionError('Offline mode must not send requests'),
    ) as send:
        invalid = http(
            '--offline',
            'https://this-should.never-resolve/foo',
            f'attachment@{FILE_PATH_ARG}',
            tolerate_error_exit_status=True,
        )
        assert invalid.exit_status == ExitStatus.ERROR
        assert 'Invalid file fields' in invalid.stderr
        assert 'perhaps you meant --form?' in invalid.stderr
        assert 'attachment' in invalid.stderr
        assert 'Traceback' not in invalid.stderr
        assert not invalid

        corrected = http(
            '--offline',
            '--form',
            'https://this-should.never-resolve/foo',
            f'attachment@{FILE_PATH_ARG}',
        )
        assert corrected.exit_status == ExitStatus.SUCCESS
        assert 'POST /foo' in corrected
        assert 'multipart/form-data' in corrected
        assert 'name="attachment"' in corrected
        assert FILE_CONTENT in corrected
        send.assert_not_called()
