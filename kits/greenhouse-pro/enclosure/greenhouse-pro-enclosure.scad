// Greenhouse Pro controller enclosure.
// OpenSCAD source for a simple printable IP65-style project box insert.

wall = 2.4;
box_x = 120;
box_y = 80;
box_z = 46;
lid_z = 3;

module rounded_box(x, y, z, r) {
  hull() {
    translate([r, r, 0]) cylinder(h = z, r = r, $fn = 32);
    translate([x - r, r, 0]) cylinder(h = z, r = r, $fn = 32);
    translate([r, y - r, 0]) cylinder(h = z, r = r, $fn = 32);
    translate([x - r, y - r, 0]) cylinder(h = z, r = r, $fn = 32);
  }
}

module base() {
  difference() {
    rounded_box(box_x, box_y, box_z, 6);
    translate([wall, wall, wall])
      rounded_box(box_x - 2 * wall, box_y - 2 * wall, box_z, 4);
    translate([12, -1, 18]) rotate([90, 0, 0]) cylinder(h = 6, r = 5, $fn = 32);
    translate([34, -1, 18]) rotate([90, 0, 0]) cylinder(h = 6, r = 5, $fn = 32);
    translate([56, -1, 18]) rotate([90, 0, 0]) cylinder(h = 6, r = 5, $fn = 32);
    translate([86, -1, 18]) rotate([90, 0, 0]) cylinder(h = 6, r = 6, $fn = 32);
  }

  // Board standoffs.
  for (p = [[22, 18], [78, 18], [22, 56], [78, 56]]) {
    translate([p[0], p[1], wall])
      difference() {
        cylinder(h = 8, r = 3.2, $fn = 24);
        translate([0, 0, -1]) cylinder(h = 10, r = 1.35, $fn = 20);
      }
  }
}

module lid() {
  translate([0, box_y + 10, 0])
    difference() {
      rounded_box(box_x, box_y, lid_z, 6);
      translate([10, 10, -1]) cylinder(h = 5, r = 1.7, $fn = 20);
      translate([box_x - 10, 10, -1]) cylinder(h = 5, r = 1.7, $fn = 20);
      translate([10, box_y - 10, -1]) cylinder(h = 5, r = 1.7, $fn = 20);
      translate([box_x - 10, box_y - 10, -1]) cylinder(h = 5, r = 1.7, $fn = 20);
    }
}

base();
lid();

