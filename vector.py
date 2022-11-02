"""
Vector
Craig Cochrane 2022

Vector data type that can perform all mathematical vector operations
"""
import math

#========== Vector Class Definition ==========
class vector:
    def __init__(self, x=0,y=0,z=None):
        """
        Method to initialise the vector object. Assigns values for x, y and z and calls the update() method to assign the meta variables
        x and y default to 0 and z defaults to None
        """
        self.x = x
        self.y = y
        self.z = z

        #Set a variable with the dimension of the vector
        if self.z == None:
            self.dimension = 2
        else:
            self.dimension = 3

        #Set a variable with the magnitude of the vector
        self.mag = self.magnitude()

        #Set a variable (of type vector) with a unit vector in the direction of this vector object
        self.unit = self.unit()

    def __str__(self):
        """
        Method to print the vector in a human readable format
        """
        if self.dimension == 2:
            vector = "({},{})".format(self.x,self.y)
        else:
            vector = "({},{},{})".format(self.x,self.y,self.z)
        return vector
    
    def __repr__(self):
        """
        Method to print a python representation of the object, which can be used to create a new object using the eval() function
        """
        if self.dimension == 2:
            vector = "vector({},{})".format(self.x,self.y)
        else:
            vector = "vector({},{},{})".format(self.x,self.y,self.z)
        return vector

    def __abs__(self):
        """
        Method to return the magnitude of the vector when the abs() function is called on it
        """
        return self.mag

    def __eq__(self, other):
        """
        Method to compare the vector object using the == equality comparison.
        The != inequality comparison is taken to be the opposite of this by default.
        
        If the other object being compared is a vector then this function returns True when the x,y and z components are all equal.
        If the other object is not a vector then it catches this and returns False.
        """
        try:
            if self.x == other.x and self.y == other.y and self.z == other.z:
                return True
            else:
                return False
        except AttributeError:
            #Runs when the other object being compared does not have an x,y or z attribute (i.e. is not a vector)
            return False

    def __add__(self, other):
        """
        Method to add two vectors using the + operator.
        If the other object is not a vector, a TypeError will be raised.
        """
        x = self.x + other.x
        y = self.y + other.y
        if self.dimension == 3:
            z = (self.z + other.z) if other.dimension==3 else self.z
        else:
            z = other.z if other.dimension==3 else None

        return vector(x,y,z)

    def __sub__(self, other):
        """
        Method to take one vvector away from another using the - operator.
        If the other object is not a vector, a TypeError will be raised.
        """
        x = self.x - other.x
        y = self.y - other.y
        if self.dimension == 3:
            z = (self.z - other.z) if other.dimension==3 else self.z
        else:
            z = (-1*other.z) if other.dimension==3 else None

        return vector(x,y,z)

    def __mul__(self, other):
        """
        Method to multiply a vector. If the other object passed in is a vector, the cross product is returned. If the other object is an int or float then the vector will be multiplied by a scalar
        If the other object is not an integer, float or vector, a TypeError will be raised.

        Only works when the vector is before the * operator as int type has no method for multiplying a vector.
        """
        if str(type(other)) == "<class '__main__.vector'>" or str(type(other)) == "<class 'vector.vector'>":
            mult = self.cross(other)
        else:
            x = self.x * other
            y = self.y * other
            if self.dimension == 3:
                z = self.z * other
            else:
                z = None

            mult = vector(x,y,z)

        return mult

    def __truediv__(self, other):
        """
        Method to divide a vector by a scalar.
        If the other object is not an integer or float, a TypeError will be raised.
        """
        x = self.x / other
        y = self.y / other
        if self.dimension == 3:
            z = self.z / other
        else:
            z = None

        return vector(x,y,z)

    def __getitem__(self, num):
        """
        Method to make the vector object subscriptable
        """
        item = None
        if num == 0:
            item = self.x
        elif num == 1:
            item = self.y
        elif item == 2:
            item = self.z
        else:
            raise IndexError("Index out of Bounds")

        return item

    def dot(self, other):
        """
        Method to return the dot product with the vector passed in as other
        """
        dot = (self.x*other.x) + (self.y*other.y)
        if self.dimension == 3 and other.dimension == 3:
            dot += (self.z*other.z)

        return dot

    def cross(self, other):
        """
        Method to return the cross product with the vector passed in as other
        """
        if self.dimension == other.dimension and self.dimension == 3:
            cross = vector(((self.y*other.z)-(self.z*other.y)), ((self.z*other.x)-(self.x*other.z)), ((self.x*other.y)-(self.y*other.x)))
        elif self.dimension == other.dimension and self.dimension == 2:
            cross = vector(0, 0, (self.x*other.y-self.y*other.x))
        elif self.dimension == 2:
            self.z = 0
            cross = vector(((self.y*other.z)-(self.z*other.y)), ((self.z*other.x)-(self.x*other.z)), ((self.x*other.y)-(self.y*other.x)))
        elif other.dimesnion == 2:
            other.z = 0
            cross = vector(((self.y*other.z)-(self.z*other.y)), ((self.z*other.x)-(self.x*other.z)), ((self.x*other.y)-(self.y*other.x)))

        return cross

    def angle(self, other=None):
        """
        Method to return the angle between this vector and another passed in as other.

        If no other vector is passed in, it defaults to the angle between the vector and the x axis
        """
        if other ==  None:
            other = vector(1,0,0)

        angle = math.acos(self.dot(other) / (self.mag * other.mag))

        return angle
        
    def magnitude(self):
        """
        Method to return the magnitude of the vector
        """
        #Ternary operation so that z is only added when it is != None
        mag = (self.x**2+self.y**2)**0.5 if self.z==None else (self.x**2+self.y**2+self.z**2)**0.5
        return mag

    def unit(self):
        """
        Method to return a unit vector in the unit of the vector
        """
        if self.mag != 0 and self.mag != 1:
            x = self.x / self.mag
            y = self.y / self.mag
            if self.dimension == 3:
                z = self.z / self.mag
            else:
                z = None
            unit = vector(x,y,z)
        
        else:
            unit = self

        return unit
