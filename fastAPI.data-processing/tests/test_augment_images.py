import numpy as np
from PIL import Image as PILImage
from app.services.images.augmentation import augment_images_from_minio

def test_augment_images_from_minio(mocker):
    # 1. Fausse image (RGB 224x224)
    dummy_img = PILImage.fromarray(np.random.randint(0, 255, (300, 300, 3), dtype=np.uint8))

    # 2. Mock des fonctions minio
    mocker.patch("app.services.images.augmentation.get_image_from_minio", return_value=dummy_img)
    mock_save = mocker.patch("app.services.images.augmentation.save_image_to_minio")

    # 3. Images d’entrée
    test_images = [
        ("test_img_1.jpg", "forest"),
        ("test_img_2.jpg", "sea"),
    ]

    # 4. Appel de la fonction
    augment_images_from_minio(
        images=test_images,
        n_aug_per_image=2,
        naming="unit_test",
        train_ratio=0.5,
    )

    # 5. Vérifications
    assert mock_save.call_count == 4  # 2 images * 2 augmentations
    for call in mock_save.call_args_list:
        args, kwargs = call
        img, key, bucket = kwargs["image"], kwargs["key"], kwargs["bucket"]
        assert isinstance(img, PILImage.Image)
        assert "unit_test/images/" in key
        assert bucket == "training-data"  # ou PIPELINE_BUCKET selon ton code
