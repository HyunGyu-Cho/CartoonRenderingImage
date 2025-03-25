import cv2
import numpy as np

def my_cartoonize_image(input_image_path: str, output_image_path: str):
    """
    나만의 알고리즘을 이용해 이미지를 만화 스타일로 변환합니다.
    
    1. 이미지를 축소한 후 다중 Bilateral Filtering을 적용하여 색 영역을 부드럽게 만듭니다.
    2. 원본 이미지를 그레이스케일로 변환하고 Gaussian Blur와 Laplacian 연산자를 이용해 엣지를 검출합니다.
    3. 검출된 엣지에 이진화 및 형태학적 팽창을 적용하여 경계선을 강화합니다.
    4. 부드러운 색상 이미지와 엣지 마스크를 결합하여 최종 만화 효과 이미지를 생성합니다.
    """
    # 1. 원본 이미지 로드
    img = cv2.imread(input_image_path)
    if img is None:
        raise FileNotFoundError(f"입력 이미지 파일을 찾을 수 없습니다: {input_image_path}")

    # 2. 이미지 축소 (처리 속도 향상 및 필터 효과 개선)
    img_small = cv2.pyrDown(img)

    # 3. 다중 Bilateral Filtering 적용 (색 영역 부드럽게)
    num_bilateral = 7
    for _ in range(num_bilateral):
        img_small = cv2.bilateralFilter(img_small, d=9, sigmaColor=75, sigmaSpace=75)

    # 4. 업스케일하여 원본 크기로 복원
    img_filtered = cv2.pyrUp(img_small)
    if img_filtered.shape != img.shape:
        img_filtered = cv2.resize(img_filtered, (img.shape[1], img.shape[0]))

    # 5. 그레이스케일 변환 후 Gaussian Blur로 노이즈 제거
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_blurred = cv2.GaussianBlur(gray, (7, 7), 0)

    # 6. Laplacian을 이용한 엣지 검출 후 이진화
    laplacian = cv2.Laplacian(gray_blurred, cv2.CV_8U, ksize=5)
    ret, edge_mask = cv2.threshold(laplacian, 80, 255, cv2.THRESH_BINARY_INV)

    # 7. 형태학적 팽창으로 엣지 강화 (엣지 두께 조절)
    kernel = np.ones((3, 3), np.uint8)
    edge_mask = cv2.dilate(edge_mask, kernel, iterations=1)

    # 8. 부드러운 색상 이미지와 엣지 마스크 결합
    cartoon = cv2.bitwise_and(img_filtered, img_filtered, mask=edge_mask)

    # 9. 결과 이미지 저장
    cv2.imwrite(output_image_path, cartoon)
    print(f"만화 스타일 이미지가 저장되었습니다: {output_image_path}")


def main():
    # 기본 경로 설정: C:\Cho\seoultech\25-1\ComputerVision
    base_path = r"C:\Cho\seoultech\25-1\ComputerVision"

    # Good 예시: photo.jpg를 변환
    good_input = base_path + r"\photo.jpg"
    good_output = base_path + r"\photo_cartoon.jpg"
    my_cartoonize_image(good_input, good_output)

    # Bad 예시: tracer.jpg를 변환
    bad_input = base_path + r"\tracer.jpg"
    bad_output = base_path + r"\tracer_cartoon.jpg"
    my_cartoonize_image(bad_input, bad_output)

    # 결과 이미지 읽기
    good_cartoon = cv2.imread(good_output)
    bad_cartoon = cv2.imread(bad_output)

    # 결과 이미지 각각 별도의 창에서 표시
    cv2.imshow("Good Cartoon", good_cartoon)
    cv2.imshow("Bad Cartoon", bad_cartoon)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
