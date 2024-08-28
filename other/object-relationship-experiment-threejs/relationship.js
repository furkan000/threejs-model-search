class Box3D {
    constructor(minX, minY, minZ, maxX, maxY, maxZ) {
        this.min = { x: minX, y: minY, z: minZ };
        this.max = { x: maxX, y: maxY, z: maxZ };
    }

    // Check if this box contains another box
    contains(other) {
        return this.min.x <= other.min.x && this.max.x >= other.max.x &&
               this.min.y <= other.min.y && this.max.y >= other.max.y &&
               this.min.z <= other.min.z && this.max.z >= other.max.z;
    }

    // Check if this box is contained by another box
    containedBy(other) {
        return other.contains(this);
    }

    // Check if this box overlaps with another box
    overlaps(other) {
        return this.min.x < other.max.x && this.max.x > other.min.x &&
               this.min.y < other.max.y && this.max.y > other.min.y &&
               this.min.z < other.max.z && this.max.z > other.min.z;
    }

    // Check if this box meets (touches) another box
    meets(other) {
        return (this.min.x === other.max.x || this.max.x === other.min.x ||
                this.min.y === other.max.y || this.max.y === other.min.y ||
                this.min.z === other.max.z || this.max.z === other.min.z)
    }

    // Determine the relationship between this box and another box
    determineRelationship(other) {
        if (this.contains(other)) {
            return 'contains';
        } else if (this.containedBy(other)) {
            return 'contained by';
        } else if (this.overlaps(other)) {
            return 'overlaps';
        } else if (this.meets(other)) {
            return 'meets';
        } else {
            return 'disjoint';
        }
    }
}