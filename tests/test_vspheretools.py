# -*- coding: utf-8 -*-

import pytest
import VSphereTools


class TestVSphereTools():

    @pytest.fixture(scope='class', autouse=True)
    def init(self):
        VSphereTools.LOGGER.setLevel(50)  # Disable debug logging while test
        # sphere = VSphereTools.Sphere()

    def test_Version(self):
        assert isinstance(VSphereTools.Version(True), str), 'Input: [ True ] expected output: [ isinstance(True, str) == True]'
        assert isinstance(VSphereTools.Version(False), str), 'Input: [ False ] expected output: [ isinstance(False, str) == True]'
