import math
from typing import List


class Vector:
    def __init__(self, coordintes: List[float]) -> None:
        """
        Initialize a vector with a list of coordinates.

        Args:
            coordinates (List[float]): List of vector components.
        """
        self.coordinates = coordintes

    def copy(v: "Vector") -> "Vector":
        """
        Create a copy of the vector.

        Args:
            v (Vector): Vector to be copied.

        Returns:
            Vector: A new vector with the same coordinates.
        """
        return Vector(v.coordinates)

    def scalar_product(v_1: "Vector", v_2: "Vector") -> float:
        """
        Compute the scalar product of two vectors.
        If vectors have different lengths, only matching components are multiplied.

        Args:
            v_1 (Vector): First vector.
            v_2 (Vector): Second vector.

        Returns:
            float: Resulting scalar product.
        """
        len_v_1 = len(v_1.coordinates)
        len_v_2 = len(v_2.coordinates)

        product: float = 0
        if len_v_1 >= len_v_2:
            for i in range(len_v_2):
                product += v_1.coordinates[i] * v_2.coordinates[i]
        else:
            for i in range(len_v_1):
                product += v_1.coordinates[i] * v_2.coordinates[i]

        return product

    def get_len(self) -> float:
        """
        Compute the Euclidean norm (length) of the vector.

        Returns:
            float: Vector length.
        """
        return math.sqrt(Vector.scalar_product(self, self))

    def get_angle(v1: "Vector", v2: "Vector") -> float:
        """
        Calculate the angle between two vectors in degrees.

        Args:
            v1 (Vector): First vector.
            v2 (Vector): Second vector.

        Returns:
            float: Angle in degrees.
        """
        return math.degrees(
            math.acos(
                Vector.scalar_product(v1, v2)
                / (Vector.get_len(v1) * Vector.get_len(v2))
            )
        )

    def __add__(self, v: "Vector") -> "Vector":
        """
        Add two vectors. If lengths differ, missing components are treated as zero.

        Args:
            v (Vector): Vector to add.

        Returns:
            Vector: Resulting vector.
        """
        res: List[float] = []
        len_self = len(self.coordinates)
        len_v = len(v.coordinates)

        if len_v >= len_self:
            for i in range(len_self):
                res.append(self.coordinates[i] + v.coordinates[i])
            for i in range(len_self, len_v):
                res.append(v.coordinates[i])
        else:
            for i in range(len_v):
                res.append(self.coordinates[i] + v.coordinates[i])
            for i in range(len_v, len_self):
                res.append(self.coordinates[i])

        return Vector(res)

    def __mul__(self, scalar: float) -> "Vector":
        """
        Multiply the vector by a scalar.

        Args:
            scalar (float): Scalar multiplier.

        Returns:
            Vector: Scaled vector.
        """
        res: List[float] = []
        for i in range(len(self.coordinates)):
            res.append(self.coordinates[i] * scalar)
        return Vector(res)

    def __sub__(self, v: "Vector") -> "Vector":
        """
        Subtract a vector (implemented via addition with a negated vector).

        Args:
            v (Vector): Vector to subtract.

        Returns:
            Vector: Resulting vector.
        """
        return self + v * (-1)

    def __repr__(self) -> str:
        """
        Return a string representation of the vector.

        Returns:
            str: String in the format `Vector([x1, x2, ...])`.
        """
        return f"Vector({self.coordinates})"


class Matrix:
    def __init__(self, m: List[List[float]]) -> None:
        """
        Initialize a matrix with a 2D list of elements.

        Args:
            m (List[List[float]]): 2D list representing the matrix.
        """
        self.elements = m

    def copy(m: "Matrix") -> "Matrix":
        """
        Create a deep copy of the matrix.

        Args:
            m (Matrix): Matrix to be copied.

        Returns:
            Matrix: A new matrix with the same elements.
        """
        return Matrix(m.elements)

    def __add__(self, m: "Matrix") -> "Matrix":
        """
        Add two matrices. Matrices must have the same dimensions.

        Args:
            m (Matrix): Matrix to add.

        Returns:
            Matrix: Resulting matrix.

        Raises:
            ValueError: If matrices have incompatible dimensions.
        """
        if len(self.elements) != len(m.elements) and len(self.elements[0]) != len(
            m.elements[0]
        ):
            raise ValueError("Matrices must have the same dimensions")
        return Matrix(
            [
                [
                    self.elements[i][j] + m.elements[i][j]
                    for j in range(len(self.elements[0]))
                ]
                for i in range(len(self.elements))
            ]
        )

    def multiplication(m_1: "Matrix", m_2: "Matrix") -> "Matrix":
        """
        Multiply two matrices. The number of columns in the first matrix must equal
        the number of rows in the second matrix.

        Args:
            m_1 (Matrix): First matrix.
            m_2 (Matrix): Second matrix.

        Returns:
            Matrix: Product matrix.

        Raises:
            ValueError: If matrices have incompatible dimensions.
        """
        if len(m_1.elements) != len(m_2.elements[0]):
            raise ValueError("Matrices must have the same dimensions")
        return Matrix(
            [
                [
                    sum(
                        m_1.elements[i][r] * m_2.elements[r][j]
                        for r in range(len(m_1.elements[0]))
                    )
                    for j in range(len(m_2.elements[0]))
                ]
                for i in range(len(m_1.elements))
            ]
        )

    def __mul__(self, scalar: float) -> "Matrix":
        """
        Multiply the matrix by a scalar.

        Args:
            scalar (float): Scalar multiplier.

        Returns:
            Matrix: Scaled matrix.
        """
        return Matrix(
            [
                [self.elements[i][j] * scalar for j in range(len(self.elements[0]))]
                for i in range(len(self.elements))
            ]
        )

    def transpose(self) -> "Matrix":
        """
        Transpose the matrix (rows become columns and vice versa).

        Returns:
            Matrix: Transposed matrix.
        """
        return Matrix(
            [
                [self.elements[i][j] for i in range(len(self.elements))]
                for j in range(len(self.elements[0]))
            ]
        )

    def __sub__(self, m: "Matrix") -> "Matrix":
        """
        Subtract a matrix (implemented via addition with a negated matrix).

        Args:
            m (Matrix): Matrix to subtract.

        Returns:
            Matrix: Resulting matrix.
        """
        return self + m * (-1)

    def __repr__(self) -> str:
        """
        Return a string representation of the matrix.

        Returns:
            str: String in the format `Matrix([[a11, a12, ...], ...])`.
        """
        return f"Matrix({self.elements})"
