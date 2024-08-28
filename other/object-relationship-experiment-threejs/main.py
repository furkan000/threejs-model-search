class Box3D:
    def __init__(self, length, width, height, x_position, y_position, z_position):
        self.length = length
        self.width = width
        self.height = height
        self.x_position = x_position
        self.y_position = y_position
        self.z_position = z_position

    def _is_disjoint(self, other):
        # Two boxes are disjoint if one box is on the 'far side' of the other in any dimension
        return (self.x_position + self.length <= other.x_position or
                other.x_position + other.length <= self.x_position or
                self.y_position + self.width <= other.y_position or
                other.y_position + other.width <= self.y_position or
                self.z_position + self.height <= other.z_position or
                other.z_position + other.height <= self.z_position)

    def _is_meet(self, other):
        # Two boxes meet if they share a common edge or point but do not overlap
        def on_edge(a_min, a_max, b_min, b_max):
            return a_max == b_min or b_max == a_min

        x_meet = on_edge(self.x_position, self.x_position + self.length,
                         other.x_position, other.x_position + other.length)
        y_meet = on_edge(self.y_position, self.y_position + self.width,
                         other.y_position, other.y_position + other.width)
        z_meet = on_edge(self.z_position, self.z_position + self.height,
                         other.z_position, other.z_position + other.height)

        return (x_meet and y_meet) or (x_meet and z_meet) or (y_meet and z_meet)

    def _is_overlap(self, other):
        # Two boxes overlap if they intersect in all three dimensions
        return not self._is_disjoint(other) and not self._is_meet(other)

    def _is_contain(self, other):
        # A box contains the other if all its 'max' dimensions are greater than those of the other box
        return (self.x_position <= other.x_position and
                self.y_position <= other.y_position and
                self.z_position <= other.z_position and
                self.x_position + self.length >= other.x_position + other.length and
                self.y_position + self.width >= other.y_position + other.width and
                self.z_position + self.height >= other.z_position + other.height)

    def _is_contained_by(self, other):
        # A box is contained by the other if all its 'max' dimensions are less than or equal to those of the other box
        return other._is_contain(self)

    def determine_relationship(self, other):
        if self._is_contain(other):
            return "contains"
        elif self._is_contained_by(other):
            return "is contained by"
        elif self._is_overlap(other):
            return "overlaps"
        elif self._is_meet(other):
            return "meets"
        else:
            return "is disjoint"


def test_determine_relationship():
    # Test for disjoint boxes
    box1 = Box3D(2, 2, 2, 0, 0, 0)
    box2 = Box3D(2, 2, 2, 5, 5, 5)
    print(box1.determine_relationship(box2))
    assert box1.determine_relationship(box2) == "is disjoint"

    # Test for meeting boxes
    box1 = Box3D(2, 2, 2, 0, 0, 0)
    box2 = Box3D(2, 2, 2, 2, 2, 2)
    print(box1.determine_relationship(box2))
    assert box1.determine_relationship(box2) == "meets"

    # Test for overlapping boxes
    box1 = Box3D(3, 3, 3, 0, 0, 0)
    box2 = Box3D(3, 3, 3, 1, 1, 1)
    print(box1.determine_relationship(box2))
    assert box1.determine_relationship(box2) == "overlaps"

    # Test for a box containing another
    box1 = Box3D(4, 4, 4, 0, 0, 0)
    box2 = Box3D(2, 2, 2, 1, 1, 1)
    print(box1.determine_relationship(box2))
    assert box1.determine_relationship(box2) == "contains"

    # Test for a box being contained by another
    box1 = Box3D(2, 2, 2, 1, 1, 1)
    box2 = Box3D(4, 4, 4, 0, 0, 0)
    print(box1.determine_relationship(box2))
    assert box1.determine_relationship(box2) == "is contained by"
    
    print("All tests passed!")

# Run the test cases
test_determine_relationship()
