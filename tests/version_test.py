#
# Copyright (c) 2021-2022 Carsten Igel.
#
# This file is part of pdm-bump
# (see https://github.com/carstencodes/pdm-bump).
#
# This file is published using the MIT license.
# Refer to LICENSE for more information
#

import unittest

from typing import Tuple, List, Final, final

from pdm_bump.version import Version, VersionParserError, Pep440VersionFormatter, BaseVersion

@final
class ParseVersionTest(unittest.TestCase):
    SUB_TESTS_VERSION_FROM_STR_RLS: Final[List[Tuple[str, str, Tuple[int, int, int]]]] = [
        ("Regular default version", "1.0.0", (1, 0, 0)),
        ("Regular default version no micro", "1.0", (1, 0, 0)),
        ("Regular default version no minor and no micro", "1", (1, 0, 0)),
        ("Pre-fixed default version", "v1.0.0", (1, 0, 0)),
        ("Pre-fixed default version no micro", "v1.0", (1, 0, 0)),
        ("Pre-fixed default version no minor and no micro", "v1", (1, 0, 0)),
        ("Regular non-final version", "0.1.0", (0, 1, 0)),
        ("Regular non-final version no micro", "0.1.0", (0, 1, 0)),
        ("Pre-fixed non-final version", "v0.1.0", (0, 1, 0)),
        ("Pre-fixed non-final version no micro", "v0.1", (0, 1, 0)),
        ("Regular version", "6.2.13", (6, 2, 13)),
        ("Regular version no micro", "6.2", (6, 2, 0)),
        ("Regular version no minor and no micro", "6", (6, 0, 0)),
        ("Pre-fixed version", "v6.2.13", (6, 2, 13)),
        ("Pre-fixed version no micro", "v6.2", (6, 2, 0)),
        ("Pre-fixed version no minor and no micro", "v6", (6, 0, 0)),
        ("Regular double-digit version", "19.22.83", (19, 22, 83)),
        ("Regular double-digit version no micro", "19.22", (19, 22, 0)),
        ("Regular double-digit version no minor and no micro", "19", (19, 0, 0)),
        ("Pre-fixed double-digit version", "v19.22.83", (19, 22, 83)),
        ("Pre-fixed double-digit version no micro", "v19.22", (19, 22, 0)),
        ("Pre-fixed double-digit version no minor and no micro", "v19", (19, 0, 0)),
    ]
    SUB_TESTS_VERSION_FROM_STR_EPOCH: Final[List[Tuple[str, str, int]]] = [
        ("No epoch set", "1.0.0", 0),
        ("Epoch is one", "1!1.0.0", 1),
        ("Epoch is double-digit", "17!1.0.0", 17),
    ]
    SUB_TESTS_VERSION_FROM_STR_PRE: Final[List[Tuple[str, str, Tuple[str, int]]]] = [
        ("None: Alpha short single digit no prefix", "0.1.0a1", ("a", 1)),
        ("None: Alpha long single digit no prefix", "0.1.0alpha1", ("a", 1)),
        ("None: Alpha short single digit prefix", "v0.1.0a1", ("a", 1)),
        ("None: Alpha long single digit prefix", "v0.1.0alpha1", ("a", 1)),
        ("None: Alpha short double digit no prefix", "0.1.0a23", ("a", 23)),
        ("None: Alpha long double digit no prefix", "0.1.0alpha23", ("a", 23)),
        ("None: Alpha short double digit prefix", "v0.1.0a23", ("a", 23)),
        ("None: Alpha long double digit prefix", "v0.1.0alpha23", ("a", 23)),
        ("None: Beta short single digit no prefix", "0.1.0b1", ("b", 1)),
        ("None: Beta long single digit no prefix", "0.1.0beta1", ("b", 1)),
        ("None: Beta short single digit prefix", "v0.1.0b1", ("b", 1)),
        ("None: Beta long single digit prefix", "v0.1.0beta1", ("b", 1)),
        ("None: Beta short double digit no prefix", "0.1.0b42", ("b", 42)),
        ("None: Beta long double digit no prefix", "0.1.0beta42", ("b", 42)),
        ("None: Beta short double digit prefix", "v0.1.0b42", ("b", 42)),
        ("None: Beta long double digit prefix", "v0.1.0beta42", ("b", 42)),
        ("None: Release-candidate short single digit no prefix", "0.1.0rc1", ("rc", 1)),
        ("None: Release-candidate long single digit no prefix", "0.1.0rc1", ("rc", 1)),
        ("None: Release-candidate short single digit prefix", "v0.1.0c1", ("rc", 1)),
        ("None: Release-candidate long single digit prefix", "v0.1.0rc1", ("rc", 1)),
        ("None: Release-candidate short double digit no prefix", "0.1.0rc99", ("rc", 99)),
        ("None: Release-candidate long double digit no prefix", "0.1.0rc99", ("rc", 99)),
        ("None: Release-candidate short double digit prefix", "v0.1.0c99", ("rc", 99)),
        ("None: Release-candidate long double digit prefix", "v0.1.0rc99", ("rc", 99)),
        ("Dot: Alpha short single digit no prefix", "0.1.0.a1", ("a", 1)),
        ("Dot: Alpha long single digit no prefix", "0.1.0.alpha1", ("a", 1)),
        ("Dot: Alpha short single digit prefix", "v0.1.0.a1", ("a", 1)),
        ("Dot: Alpha long single digit prefix", "v0.1.0.alpha1", ("a", 1)),
        ("Dot: Alpha short double digit no prefix", "0.1.0.a23", ("a", 23)),
        ("Dot: Alpha long double digit no prefix", "0.1.0.alpha23", ("a", 23)),
        ("Dot: Alpha short double digit prefix", "v0.1.0.a23", ("a", 23)),
        ("Dot: Alpha long double digit prefix", "v0.1.0.alpha23", ("a", 23)),
        ("Dot: Beta short single digit no prefix", "0.1.0.b1", ("b", 1)),
        ("Dot: Beta long single digit no prefix", "0.1.0.beta1", ("b", 1)),
        ("Dot: Beta short single digit prefix", "v0.1.0.b1", ("b", 1)),
        ("Dot: Beta long single digit prefix", "v0.1.0.beta1", ("b", 1)),
        ("Dot: Beta short double digit no prefix", "0.1.0.b42", ("b", 42)),
        ("Dot: Beta long double digit no prefix", "0.1.0.beta42", ("b", 42)),
        ("Dot: Beta short double digit prefix", "v0.1.0.b42", ("b", 42)),
        ("Dot: Beta long double digit prefix", "v0.1.0.beta42", ("b", 42)),
        ("Dot: Release-candidate short single digit no prefix", "0.1.0.rc1", ("rc", 1)),
        ("Dot: Release-candidate long single digit no prefix", "0.1.0.rc1", ("rc", 1)),
        ("Dot: Release-candidate short single digit prefix", "v0.1.0.c1", ("rc", 1)),
        ("Dot: Release-candidate long single digit prefix", "v0.1.0.rc1", ("rc", 1)),
        ("Dot: Release-candidate short double digit no prefix", "0.1.0.rc99", ("rc", 99)),
        ("Dot: Release-candidate long double digit no prefix", "0.1.0.rc99", ("rc", 99)),
        ("Dot: Release-candidate short double digit prefix", "v0.1.0.c99", ("rc", 99)),
        ("Dot: Release-candidate long double digit prefix", "v0.1.0.rc99", ("rc", 99)),
        ("Hyphen: Alpha short single digit no prefix", "0.1.0-a1", ("a", 1)),
        ("Hyphen: Alpha long single digit no prefix", "0.1.0-alpha1", ("a", 1)),
        ("Hyphen: Alpha short single digit prefix", "v0.1.0-a1", ("a", 1)),
        ("Hyphen: Alpha long single digit prefix", "v0.1.0-alpha1", ("a", 1)),
        ("Hyphen: Alpha short double digit no prefix", "0.1.0-a23", ("a", 23)),
        ("Hyphen: Alpha long double digit no prefix", "0.1.0-alpha23", ("a", 23)),
        ("Hyphen: Alpha short double digit prefix", "v0.1.0-a23", ("a", 23)),
        ("Hyphen: Alpha long double digit prefix", "v0.1.0-alpha23", ("a", 23)),
        ("Hyphen: Beta short single digit no prefix", "0.1.0-b1", ("b", 1)),
        ("Hyphen: Beta long single digit no prefix", "0.1.0-beta1", ("b", 1)),
        ("Hyphen: Beta short single digit prefix", "v0.1.0-b1", ("b", 1)),
        ("Hyphen: Beta long single digit prefix", "v0.1.0-beta1", ("b", 1)),
        ("Hyphen: Beta short double digit no prefix", "0.1.0-b42", ("b", 42)),
        ("Hyphen: Beta long double digit no prefix", "0.1.0-beta42", ("b", 42)),
        ("Hyphen: Beta short double digit prefix", "v0.1.0-b42", ("b", 42)),
        ("Hyphen: Beta long double digit prefix", "v0.1.0-beta42", ("b", 42)),
        ("Hyphen: Release-candidate short single digit no prefix", "0.1.0-rc1", ("rc", 1)),
        ("Hyphen: Release-candidate long single digit no prefix", "0.1.0-rc1", ("rc", 1)),
        ("Hyphen: Release-candidate short single digit prefix", "v0.1.0-c1", ("rc", 1)),
        ("Hyphen: Release-candidate long single digit prefix", "v0.1.0-rc1", ("rc", 1)),
        ("Hyphen: Release-candidate short double digit no prefix", "0.1.0-rc99", ("rc", 99)),
        ("Hyphen: Release-candidate long double digit no prefix", "0.1.0-rc99", ("rc", 99)),
        ("Hyphen: Release-candidate short double digit prefix", "v0.1.0-c99", ("rc", 99)),
        ("Hyphen: Release-candidate long double digit prefix", "v0.1.0-rc99", ("rc", 99)),
        ("Underscore: Alpha short single digit no prefix", "0.1.0_a1", ("a", 1)),
        ("Underscore: Alpha long single digit no prefix", "0.1.0_alpha1", ("a", 1)),
        ("Underscore: Alpha short single digit prefix", "v0.1.0_a1", ("a", 1)),
        ("Underscore: Alpha long single digit prefix", "v0.1.0_alpha1", ("a", 1)),
        ("Underscore: Alpha short double digit no prefix", "0.1.0_a23", ("a", 23)),
        ("Underscore: Alpha long double digit no prefix", "0.1.0_alpha23", ("a", 23)),
        ("Underscore: Alpha short double digit prefix", "v0.1.0_a23", ("a", 23)),
        ("Underscore: Alpha long double digit prefix", "v0.1.0_alpha23", ("a", 23)),
        ("Underscore: Beta short single digit no prefix", "0.1.0_b1", ("b", 1)),
        ("Underscore: Beta long single digit no prefix", "0.1.0_beta1", ("b", 1)),
        ("Underscore: Beta short single digit prefix", "v0.1.0_b1", ("b", 1)),
        ("Underscore: Beta long single digit prefix", "v0.1.0_beta1", ("b", 1)),
        ("Underscore: Beta short double digit no prefix", "0.1.0_b42", ("b", 42)),
        ("Underscore: Beta long double digit no prefix", "0.1.0_beta42", ("b", 42)),
        ("Underscore: Beta short double digit prefix", "v0.1.0_b42", ("b", 42)),
        ("Underscore: Beta long double digit prefix", "v0.1.0_beta42", ("b", 42)),
        ("Underscore: Release-candidate short single digit no prefix", "0.1.0_rc1", ("rc", 1)),
        ("Underscore: Release-candidate long single digit no prefix", "0.1.0_rc1", ("rc", 1)),
        ("Underscore: Release-candidate short single digit prefix", "v0.1.0_c1", ("rc", 1)),
        ("Underscore: Release-candidate long single digit prefix", "v0.1.0_rc1", ("rc", 1)),
        ("Underscore: Release-candidate short double digit no prefix", "0.1.0_rc99", ("rc", 99)),
        ("Underscore: Release-candidate long double digit no prefix", "0.1.0_rc99", ("rc", 99)),
        ("Underscore: Release-candidate short double digit prefix", "v0.1.0_c99", ("rc", 99)),
        ("Underscore: Release-candidate long double digit prefix", "v0.1.0_rc99", ("rc", 99)),
    ]
    SUB_TESTS_VERSION_FROM_STR_DEV: Final[List[Tuple[str, str, Tuple[str, int]]]] = [
        ("Regular version zero digit none", "0.0.1dev0", ("dev", 0)),
        ("Regular version zero digit dot", "0.0.1.dev0", ("dev", 0)),
        ("Regular version zero digit hyphen", "0.0.1-dev0", ("dev", 0)),
        ("Regular version zero digit underscore", "0.0.1_dev0", ("dev", 0)),
        ("Regular version no digit none", "0.0.1dev", ("dev", 0)),
        ("Regular version no digit dot", "0.0.1.dev", ("dev", 0)),
        ("Regular version no digit hyphen", "0.0.1-dev", ("dev", 0)),
        ("Regular version no digit underscore", "0.0.1_dev", ("dev", 0)),
        ("Regular version single digit none", "0.0.1dev1", ("dev", 1)),
        ("Regular version single digit dot", "0.0.1.dev1", ("dev", 1)),
        ("Regular version single digit hyphen", "0.0.1-dev1", ("dev", 1)),
        ("Regular version single digit underscore", "0.0.1_dev1", ("dev", 1)),
        ("Regular version double digit none", "0.0.1dev57", ("dev", 57)),
        ("Regular version double digit dot", "0.0.1.dev57", ("dev", 57)),
        ("Regular version double digit hyphen", "0.0.1-dev57", ("dev", 57)),
        ("Regular version double digit underscore", "0.0.1_dev57", ("dev", 57)),
        ("Pre-fixed version single digit none", "v0.0.1dev1", ("dev", 1)),
        ("Pre-fixed version single digit dot", "v0.0.1.dev1", ("dev", 1)),
        ("Pre-fixed version single digit hyphen", "v0.0.1-dev1", ("dev", 1)),
        ("Pre-fixed version single digit underscore", "v0.0.1_dev1", ("dev", 1)),
        ("Pre-fixed version double digit none", "v0.0.1dev57", ("dev", 57)),
        ("Pre-fixed version double digit dot", "v0.0.1.dev57", ("dev", 57)),
        ("Pre-fixed version double digit hyphen", "v0.0.1-dev57", ("dev", 57)),
        ("Pre-fixed version double digit underscore", "v0.0.1_dev57", ("dev", 57)),
    ]
    SUB_TESTS_VERSION_FROM_STR_POST: Final[List[Tuple[str, str, Tuple[str, int]]]] = [
        ("Regular version zero digit none", "2.0.0post0", ("post", 0)),
        ("Regular version zero digit dot", "2.0.0.post0", ("post", 0)),
        ("Regular version zero digit hyphen", "2.0.0-post0", ("post", 0)),
        ("Regular version zero digit underscore", "2.0.0_post0", ("post", 0)),
        ("Regular version no digit none", "2.0.0post", ("post", 0)),
        ("Regular version no digit dot", "2.0.0.post", ("post", 0)),
        ("Regular version no digit hyphen", "2.0.0-post", ("post", 0)),
        ("Regular version no digit underscore", "2.0.0_post", ("post", 0)),
        ("Regular version single digit none", "2.0.0post7", ("post", 7)),
        ("Regular version single digit dot", "2.0.0.post7", ("post", 7)),
        ("Regular version single digit hyphen", "2.0.0-post7", ("post", 7)),
        ("Regular version single digit underscore", "2.0.0_post7", ("post", 7)),
        ("Regular version double digit none", "2.0.0post63", ("post", 63)),
        ("Regular version double digit dot", "2.0.0.post63", ("post", 63)),
        ("Regular version double digit hyphen", "2.0.0-post63", ("post", 63)),
        ("Regular version double digit underscore", "2.0.0_post63", ("post", 63)),
        ("Regular version single digit special form", "2.0.0-3", ("post", 3)),
        ("Regular version double digit special form", "2.0.0-78", ("post", 78)),
        ("Pre-fixed version zero digit none", "v2.0.0post0", ("post", 0)),
        ("Pre-fixed version zero digit dot", "v2.0.0.post0", ("post", 0)),
        ("Pre-fixed version zero digit hyphen", "v2.0.0-post0", ("post", 0)),
        ("Pre-fixed version zero digit underscore", "v2.0.0_post0", ("post", 0)),
        ("Pre-fixed version no digit none", "v2.0.0post", ("post", 0)),
        ("Pre-fixed version no digit dot", "v2.0.0.post", ("post", 0)),
        ("Pre-fixed version no digit hyphen", "v2.0.0-post", ("post", 0)),
        ("Pre-fixed version no digit underscore", "v2.0.0_post", ("post", 0)),
        ("Pre-fixed version single digit none", "v2.0.0post7", ("post", 7)),
        ("Pre-fixed version single digit dot", "v2.0.0.post7", ("post", 7)),
        ("Pre-fixed version single digit hyphen", "v2.0.0-post7", ("post", 7)),
        ("Pre-fixed version single digit underscore", "v2.0.0_post7", ("post", 7)),
        ("Pre-fixed version double digit none", "v2.0.0post63", ("post", 63)),
        ("Pre-fixed version double digit dot", "v2.0.0.post63", ("post", 63)),
        ("Pre-fixed version double digit hyphen", "v2.0.0-post63", ("post", 63)),
        ("Pre-fixed version double digit underscore", "v2.0.0_post63", ("post", 63)),
        ("Pre-fixed version single digit special form", "v2.0.0-3", ("post", 3)),
        ("Pre-fixed version double digit special form", "v2.0.0-78", ("post", 78)),
    ]  # TODO: rev/r
    SUB_TESTS_VERSION_FROM_STR_LOCAL: Final[List[Tuple[str, str, str]]] = [
        ("Regular version single digit plus", "3.1.4+2", "2"),
        ("Regular version double digit plus", "3.1.4+12", "12"),
        ("Regular version alpha-numeric plus", "3.1.4+af2b", "af2b"),
        ("Regular version hyphen plus", "3.1.4+just-my-2-cents", "just.my.2.cents"),
        ("Regular version hyphen underscore plus", "3.1.4+just_my-2_cents", "just.my.2.cents"),
        ("Pre-fixed version single digit plus", "v3.1.4+2", "2"),
        ("Pre-fixed version double digit plus", "v3.1.4+12", "12"),
        ("Pre-fixed version alpha-numeric plus", "v3.1.4+af2b", "af2b"),
        ("Pre-fixed version hyphen plus", "v3.1.4+just-my-2-cents", "just.my.2.cents"),
        ("Pre-fixed version hyphen underscore plus", "v3.1.4+just_my-2_cents", "just.my.2.cents"),
    ]
    SUB_TESTS_VERSION_PARSE_SUCCESS: Final[List[Tuple[str, str]]] = [
        ("Regular version", "1.2.3"),
        ("Prefixed version", "v1.2.3"),
        ("Prefixed version with alpha", "v1.2.3a4"),
        ("Prefixed version with beta", "v1.2.3b4"),
        ("Prefixed version with rc", "v1.2.3rc4"),
        ("Prefixed version with rc as post", "v1.2.3a4post5"),
        ("Prefixed version with rc as post alternative", "v1.2.3a4-5"),
        ("Prefixed version with rc as post and dev", "v1.2.3a4-post5.dev17"),
        ("Prefixed version with rc as post and dev and local", "v1.2.3a4-post5.dev17+erg.13"),
    ]
    SUB_TESTS_VERSION_PARSE_FAIL: Final[List[Tuple[str, str]]] = [
        ("Wrong prefix", "a0.1.0+2"),
        ("Negative epoch", "-2!v0.1.0+2"),
        ("Alpha epoch", "f!v0.1.0+2"),
        ("Wrong separators", "0-1-0"),
        ("Wrong alpha", "0.1.0alp1"),
        ("Wrong beta", "0.1.0bet2"),
        ("Wrong release candidate", "0.1.0relca3"),
        ("Negative major", "-1.0.0"),
        ("Negative minor", "1.-2.0"),
        ("Negative micro", "1.2.-3"),
    ]

    def test_default_version_is_one(self) -> None:
        v1: Version = Version.default()
        v2: Version = Version.from_string("1")
        self.assertEquals(v1, v2)

    def test_create_version_from_str_epoch_part(self) -> None:
        for message, version, epoch in self.SUB_TESTS_VERSION_FROM_STR_EPOCH:
            with self.subTest(message, version=version):
                v: Version = Version.from_string(version)
                self.assertEqual(v.epoch, epoch)

    def test_create_version_from_str_rls_part(self) -> None:
        for message, version, release in self.SUB_TESTS_VERSION_FROM_STR_RLS:
            with self.subTest(message, version=version):
                v: Version = Version.from_string(version)
                self.assertEqual(v.release, release)

    def test_create_version_from_str_preview_part(self) -> None:
        for message, version, preview in self.SUB_TESTS_VERSION_FROM_STR_PRE:
            with self.subTest(message, version=version):
                v: Version = Version.from_string(version)
                self.assertEqual(v.preview, preview)

    def test_create_version_from_str_dev_part(self) -> None:
        for message, version, dev in self.SUB_TESTS_VERSION_FROM_STR_DEV:
            with self.subTest(message, version=version):
                v: Version = Version.from_string(version)
                self.assertEqual(v.dev, dev)

    def test_create_version_from_str_post_part(self) -> None:
        for message, version, post in self.SUB_TESTS_VERSION_FROM_STR_POST:
            with self.subTest(message, version=version):
                v: Version = Version.from_string(version)
                self.assertEqual(v.post, post)

    def test_create_version_from_str_local_part(self) -> None:
        for message, version, local in self.SUB_TESTS_VERSION_FROM_STR_LOCAL:
            with self.subTest(message, version=version):
                v: Version = Version.from_string(version)
                self.assertEqual(v.local, local)

    def test_create_version_from_str_can_parse_success(self) -> None:
        for message, version in self.SUB_TESTS_VERSION_PARSE_SUCCESS:
            with self.subTest(message, version=version):
                result: bool = Version.can_parse_to_version(version)
                self.assertTrue(result)

    def test_create_version_from_str_can_parse_fail(self) -> None:
        for message, version in self.SUB_TESTS_VERSION_PARSE_FAIL:
            with self.subTest(message, version=version):
                result: bool = Version.can_parse_to_version(version)
                self.assertFalse(result)

    def test_create_version_from_str_parse_raises(self) -> None:
        for message, version in self.SUB_TESTS_VERSION_PARSE_FAIL:
            with self.subTest(message, version=version):
                parse = lambda version=version: Version.from_string(version)
                self.assertRaises(VersionParserError, parse)


@final
class CreateVersionTest(unittest.TestCase):
    pass  # TODO implement


@final
class VersionPropertiesTest(unittest.TestCase):
    def test_version_major(self) -> None:
        v = Version(release_tuple=(1, 2, 3))
        self.assertEqual(v.major, 1)

    def test_version_minor(self) -> None:
        v = Version(release_tuple=(1, 2, 3))
        self.assertEqual(v.minor, 2)

    def test_version_micro(self) -> None:
        v = Version(release_tuple=(1, 2, 3))
        self.assertEqual(v.micro, 3)

    def test_version_major_unset(self) -> None:
        v = Version(release_tuple=tuple())
        self.assertEqual(v.major, 0)

    def test_version_minor_unset(self) -> None:
        v = Version(release_tuple=(1,))
        self.assertEqual(v.minor, 0)

    def test_version_micro_unset(self) -> None:
        v = Version(release_tuple=(1, 2))
        self.assertEqual(v.micro, 0)

    def test_version_is_no_pre_release(self) -> None:
        v = Version(release_tuple=(1, 2, 3))
        self._assure_pre_matches(v, False, False, False, False, False)
        self.assertFalse(v.is_post_release or v.is_local_version)

    def test_version_is_alpha_true(self) -> None:
        v = self._create_version(as_alpha=True)
        self._assure_pre_matches(v, True, False, False, True, False)
        self.assertFalse(v.is_post_release or v.is_local_version)

    def test_version_is_beta_true(self) -> None:
        v = self._create_version(as_beta=True)
        self._assure_pre_matches(v, False, True, False, True, False)
        self.assertFalse(v.is_post_release or v.is_local_version)

    def test_version_is_rc_true(self) -> None:
        v = self._create_version(as_rc=True)
        self._assure_pre_matches(v, False, False, True, True, False)
        self.assertFalse(v.is_post_release or v.is_local_version)

    def test_version_is_dev_true(self) -> None:
        v = self._create_version(as_dev=True)
        self._assure_pre_matches(v, False, False, False, True, True)
        self.assertFalse(v.is_post_release or v.is_local_version)

    def test_version_is_post_true(self) -> None:
        v = self._create_version(as_post=True)
        self._assure_pre_matches(v, False, False, False, False, False)
        self.assertTrue(v.is_post_release)
        self.assertFalse(v.is_post_release and v.is_local_version)

    def test_version_is_local_true(self) -> None:
        v = self._create_version(as_local=True)
        self._assure_pre_matches(v, False, False, False, False, False)
        self.assertTrue(v.is_local_version)
        self.assertFalse(v.is_post_release and v.is_local_version)

    def _create_version(
            self,
            *,
            as_alpha: bool = False,
            as_beta: bool = False,
            as_rc: bool = False,
            as_dev: bool = False,
            as_post: bool = False,
            as_local: bool = False
            )-> Version:
        epoch = 1
        release = (2, 3, 4)
        dev = None if not as_dev else ("dev", 5)
        post = None if not as_post else ("post", 6)
        local = None if not as_local else "as.local7"

        items = int(as_alpha) + int(as_beta) + int(as_rc)
        if items > 1:
            raise ValueError("Only one pre-release identifier can be set")
        pre = None
        if as_alpha:
            pre = ("a", 8)
        elif as_beta:
            pre = ("b", 9)
        elif as_rc:
            pre = ("rc", 10)

        return Version(epoch, release, pre, post, dev, local)

    def _assure_pre_matches(self, version: Version, is_alpha, is_beta, is_rc, is_pre, is_dev) -> None:
        self.assertEqual(version.is_alpha, is_alpha)
        self.assertEqual(version.is_beta, is_beta)
        self.assertEqual(version.is_release_candidate, is_rc)
        self.assertEqual(version.is_pre_release, is_pre)
        self.assertEqual(version.is_development_version, is_dev)

@final
class VersionOrderingTest(unittest.TestCase):
    pass  # TODO implement


@final
class FormatVersionTest(unittest.TestCase):
    pass  # TODO implement


@final
class RoundtripTest(unittest.TestCase):
    pass  # TODO implement
