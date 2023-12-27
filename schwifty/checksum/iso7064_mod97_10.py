from schwifty import checksum


# Bosnia and Herzegovina (BT)
# Montenegro (ME)
# North Macedonia (MK)
# Portugal (PT)
# Serbia (RS)
# Solvenia (SI)
@checksum.register("BT", "ME", "MK", "PT", "RS", "SI")
class DefaultAlgorithm(checksum.ISO7064_mod97_10):
    name = "default"
