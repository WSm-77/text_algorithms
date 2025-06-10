import hashlib

class NilsimsHash:
    """Klasa implementująca algorytm Nilsimsa."""

    def __init__(self):
        """Inicjalizuje hash Nilsimsa."""
        self.tran = [
            0x02, 0xD6, 0x9E, 0x6F, 0xF9, 0x1D, 0x04, 0xAB, 0xD0, 0x22, 0x16, 0x1F, 0xD8, 0x73, 0xA1, 0xAC,
            0x3B, 0x70, 0x62, 0x96, 0x1E, 0x6E, 0x8F, 0x39, 0x9D, 0x05, 0x14, 0x4A, 0xA6, 0xBE, 0xAE, 0x0E,
            0xCF, 0xB9, 0x9C, 0x9A, 0xC7, 0x68, 0x13, 0xE1, 0x2D, 0xA4, 0xEB, 0x51, 0x8D, 0x64, 0x6B, 0x50,
            0x23, 0x80, 0x03, 0x41, 0xEC, 0xBB, 0x71, 0xCC, 0x7A, 0x86, 0x7F, 0x98, 0xF2, 0x36, 0x5E, 0xEE,
            0x8E, 0xCE, 0x4F, 0xB2, 0x2F, 0x40, 0x52, 0x2C, 0x8A, 0x5D, 0x74, 0x95, 0xB7, 0x5A, 0x94, 0x13,
            0x7B, 0xF1, 0x66, 0x5C, 0xC5, 0x48, 0x1C, 0xD4, 0x06, 0xB8, 0xF4, 0x0F, 0x61, 0x81, 0xD5, 0x0A,
            0x75, 0x12, 0x2A, 0x0B, 0x47, 0xDF, 0x11, 0x7C, 0xE5, 0x11, 0x3D, 0x3F, 0x5B, 0x8F, 0x66, 0x2B,
            0x18, 0xAA, 0x0A, 0x32, 0x75, 0xCC, 0xF3, 0x36, 0x65, 0x49, 0x0B, 0x16, 0x67, 0xBF, 0xE3, 0x85,
            0x4C, 0x70, 0x25, 0xB6, 0x65, 0x6F, 0x8C, 0x92, 0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA,
            0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84, 0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A,
            0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06, 0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02,
            0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B, 0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA,
            0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73, 0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85,
            0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E, 0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89,
            0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B, 0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20,
            0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4, 0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31
        ]

    def _rolling_hash(self, text: str) -> list[int]:
        """
        Oblicza rolling hash dla tekstu.

        Args:
            text: Tekst do przetworzenia

        Returns:
            Lista wartości rolling hash
        """
        n = len(text)
        if n < 3:
            return []

        hashes = []
        hash_value = 0
        for j, char in enumerate(text):
            hash_value ^= self.tran[ord(char) & 0xFF] << (j*8)
            hash_value &= 0xFFFFFFFF
            hashes.append(hash_value)

        return hashes

    def _trigrams(self, text: str) -> list[str]:
        """
        Generuje trigramy z tekstu.

        Args:
            text: Tekst do przetworzenia

        Returns:
            Lista trigramów
        """
        if len(text) < 3:
            return []

        trigrams = []
        for i in range(len(text) - 2):
            trigrams.append(text[i:i + 3])

        return trigrams

    def compute_hash(self, text: str) -> bytes:
        """
        Oblicza hash Nilsimsa dla tekstu.

        Args:
            text: Tekst do zahashowania

        Returns:
            256-bitowy hash jako bytes
        """
        if not text:
            return b'\x00' * 32

        processed_text = ''.join(c.lower() for c in text if c.isalnum() or c.isspace())
        trigrams = self._trigrams(processed_text)

        accumulator = [0] * 256

        for trigram in trigrams:
            hash_val = self._rolling_hash(trigram)[-1]

            for bit in range(8):
                bit_index = (hash_val >> (bit * 4)) & 0xFF
                if bit_index < 256:
                    accumulator[bit_index] += 1

        if len(trigrams) > 0:
            threshold = sum(accumulator) // (256 * 2)
        else:
            threshold = 0

        hash_bits = []
        for count in accumulator:
            hash_bits.append(1 if count > threshold else 0)

        hash_bytes = bytearray(32)
        for i in range(256):
            byte_index = i // 8
            bit_index = i % 8
            if hash_bits[i]:
                hash_bytes[byte_index] |= (1 << bit_index)

        return bytes(hash_bytes)

    def compare_hashes(self, hash1: bytes, hash2: bytes) -> float:
        """
        Porównuje dwa hashe Nilsimsa i zwraca stopień podobieństwa.

        Args:
            hash1: Pierwszy hash
            hash2: Drugi hash

        Returns:
            Stopień podobieństwa w zakresie [0, 1]
        """
        if len(hash1) != 32 or len(hash2) != 32:
            raise ValueError("Hash must be 32-bit")

        hamming = 0
        for byte1, byte2 in zip(hash1, hash2):
            xor = byte1 ^ byte2
            hamming += bin(xor).count('1')

        total_bits = 256
        similarity = 1.0 - (hamming / total_bits)
        return max(0.0, min(1.0, similarity))

def nilsims_similarity(text1: str, text2: str) -> float:
    """
    Oblicza podobieństwo między dwoma tekstami używając algorytmu Nilsimsa.

    Args:
        text1: Pierwszy tekst
        text2: Drugi tekst

    Returns:
        Stopień podobieństwa w zakresie [0, 1]
    """
    nh = NilsimsHash()
    hash1 = nh.compute_hash(text1)
    hash2 = nh.compute_hash(text2)
    return nh.compare_hashes(hash1, hash2)

def find_similar_texts(target: str, candidates: list[str], threshold: float = 0.7) -> list[tuple[int, float]]:
    """
    Znajduje teksty podobne do tekstu docelowego.

    Args:
        target: Tekst docelowy
        candidates: Lista kandydatów
        threshold: Próg podobieństwa

    Returns:
        Lista krotek (indeks, podobieństwo) dla tekstów powyżej progu
    """
    nh = NilsimsHash()
    hash_target = nh.compute_hash(target)

    similars = []

    for i, candidate in enumerate(candidates):
        hash_candidate = nh.compute_hash(candidate)
        probability = nh.compare_hashes(hash_target, hash_candidate)
        if probability >= threshold:
            similars.append((i, probability))
    return similars
