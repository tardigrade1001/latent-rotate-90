import torch

__all__ = [
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS",
]


class LatentRotatePortraitLandscape:
    """
    Emits latent(s) rotated at 0° and/or 90°.
    Designed for deterministic orientation comparison.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "latent": ("LATENT",),
                "mode": (["Portrait Only", "Landscape Only", "Both"],),
            }
        }

    RETURN_TYPES = ("LATENT",)
    OUTPUT_IS_LIST = (True,)
    FUNCTION = "rotate"

    CATEGORY = "latent/geometry"

    def rotate(self, latent, mode):
        print(
            "[LatentRotate] Reminder: for deterministic comparison, "
            "KSampler seed must be fixed."
        )

        results = []

        samples = latent["samples"]

        def make_latent(samples_tensor, rotation, orientation):
            return {
                "samples": samples_tensor,
                "rotation": rotation,
                "orientation": orientation,
            }

        # 0° — Portrait
        if mode in ("Portrait Only", "Both"):
            results.append(
                make_latent(samples, rotation=0, orientation="portrait")
            )

        # 90° — Landscape
        if mode in ("Landscape Only", "Both"):
            rotated = torch.rot90(samples, k=-1, dims=(2, 3))
            results.append(
                make_latent(rotated, rotation=90, orientation="landscape")
            )

        return (results,)


# --------------------------------------------------
# ComfyUI registration
# --------------------------------------------------

NODE_CLASS_MAPPINGS = {
    "LatentRotatePortraitLandscape": LatentRotatePortraitLandscape
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LatentRotatePortraitLandscape": "Latent Rotate (Portrait / Landscape)"
}
