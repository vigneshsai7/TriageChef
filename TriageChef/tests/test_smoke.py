def test_import():
    import sys; sys.path.insert(0,'src')
    import cyberchef_bridge; assert 'powershell-base64' in cyberchef_bridge.RECIPES
