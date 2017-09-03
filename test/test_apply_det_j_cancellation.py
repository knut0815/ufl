from ufl import *
from ufl.algebra import Product, Sum, Division
# from ufl.algorithms.apply_algebra_lowering import apply_algebra_lowering, apply_minimal_algebra_lowering
# from ufl.algorithms.apply_derivatives import apply_derivatives
# from ufl.algorithms.apply_function_pullbacks import apply_function_pullbacks
# from ufl.algorithms.compute_form_data import compute_form_data
from ufl.algorithms.apply_det_j_cancellation import apply_det_j_cancellation
# from ufl.algorithms.expand_indices import expand_indices
# from ufl.algorithms.apply_jacobian_cancellation import apply_jacobian_cancellation
# from ufl.constantvalue import FloatValue, Zero
# from ufl.core.multiindex import MultiIndex, FixedIndex
# from ufl.core.operator import Operator
# from ufl.corealg.traversal import post_traversal
# from ufl.differentiation import ReferenceGrad, ReferenceDiv, ReferenceCurl
from ufl.geometry import JacobianDeterminant
# from ufl.indexed import Indexed
# from ufl.indexsum import IndexSum
# from ufl.referencevalue import ReferenceValue
# from ufl.tensors import ComponentTensor
# from itertools import izip_longest
import pytest

@pytest.fixture
def detJ():
    cell = triangle
    element = FiniteElement("CG", cell, 1)
    domain = Coefficient(element).ufl_domain()
    return JacobianDeterminant(domain)

adjc = apply_det_j_cancellation

def test_basic(detJ):
    assert adjc(detJ / detJ) == 1.0
    assert adjc(detJ * (5.0/detJ)) == 5.0
    assert adjc(((5.0*detJ) + (3.0*detJ)) * (1/detJ)) == 8.0

def dont_test_tensors(detJ):
    xd = as_tensor([5.0*detJ, 3.0*detJ])
    x = as_tensor([5.0, 3.0])
    assert adjc(xd * (1/detJ)) == x # Note the general UFL bug displayed by this.
    assert adjc(xd[i] * (1/detJ)) == x[i]
    assert adjc(as_tensor(xd[i], i) * (1/detJ)) == as_tensor(x[i], i)
    
# def context():
#     class Context:
#         def return_values(self, element):
#             f = Coefficient(element)
#             g = Coefficient(element)
#             w = Argument(element, 0)
#             return f, g, w, element
#         def scalar(self, cell=triangle):
#             element = FiniteElement("Lagrange", cell, degree=1)
#             return self.return_values(element)
#         def vector(self, dim, cell=triangle):
#             element = VectorElement("Lagrange", cell, degree=1, dim=dim)
#             return self.return_values(element)
#         def tensor(self, dim1, dim2, cell=triangle):
#             element = TensorElement("Lagrange", cell, degree=1, shape=(dim1,dim2))
#             return self.return_values(element)
#         def rt(self):
#             cell = tetrahedron
#             element = FiniteElement("RT", cell, degree=1)
#             return self.return_values(element)
#         def n1curl(self):
#             cell = tetrahedron
#             element = FiniteElement("N1curl", cell, degree=1)
#             return self.return_values(element)
#     return Context()

# class TestCoefficientDerivativeOfDot:
#     def test_left_simple(self, context):
#         f, g, w, element = context.tensor(dim1=3, dim2=3)
#         base_expression = dot(f, g)
#         actual = apply_derivatives(derivative(base_expression, f, w))
#         expected = dot(w, g)
#         assert equal_up_to_index_relabelling(actual, expected)

#     def test_right_simple(self, context):
#         f, g, w, element = context.vector(dim=4)
#         base_expression = dot(f, g)
#         actual = apply_derivatives(derivative(base_expression, g, w))
#         expected = dot(f, w)
#         assert equal_up_to_index_relabelling(actual, expected)

#     def test_both_simple(self, context):
#         f, g, w, element = context.tensor(dim1=3, dim2=3)
#         base_expression = dot(f, f)
#         actual = apply_derivatives(derivative(base_expression, f, w))
#         expected = dot(w, f) + dot(f, w) # NB: not 2*dot(w, f).
#         assert equal_up_to_index_relabelling(actual, expected)

# class TestCoefficientDerivativeOfInner:
#     def test_left_simple(self, context):
#         f, g, w, element = context.tensor(dim1=2, dim2=3)
#         base_expression = inner(f, g)
#         actual = apply_derivatives(derivative(base_expression, f, w))
#         expected = inner(w, g)
#         assert equal_up_to_index_relabelling(actual, expected)

#     def test_right_simple(self, context):
#         f, g, w, element = context.vector(dim=4)
#         base_expression = inner(f, g)
#         actual = apply_derivatives(derivative(base_expression, g, w))
#         expected = inner(f, w)
#         assert equal_up_to_index_relabelling(actual, expected)

#     def test_both_simple(self, context):
#         f, g, w, element = context.tensor(dim1=3, dim2=2)
#         base_expression = inner(f, f)
#         actual = apply_derivatives(derivative(base_expression, f, w))
#         expected = inner(w, f) + inner(f, w) # NB: not 2*inner(w, f).
#         assert equal_up_to_index_relabelling(actual, expected)

# class TestCoefficientDerivativeOfGrad:
#     def test_simple(self, context):
#         f, g, w, element = context.vector(dim=3)
#         base_expression = grad(f)
#         actual = apply_derivatives(derivative(base_expression, f, w))
#         expected = grad(w)
#         assert equal_up_to_index_relabelling(actual, expected)

# class TestCoefficientDerivativeOfDiv:
#     def test_simple_2D(self, context):
#         f, g, w, element = context.vector(dim=2)
#         base_expression = div(f)
#         actual = apply_derivatives(derivative(base_expression, f, w))
#         expected = div(w)
#         assert equal_up_to_index_relabelling(actual, expected)

#     def test_simple_3D(self, context):
#         f, g, w, element = context.vector(dim=3, cell=tetrahedron)
#         base_expression = div(f)
#         actual = apply_derivatives(derivative(base_expression, f, w))
#         expected = div(w)
#         assert equal_up_to_index_relabelling(actual, expected)

# class TestCoefficientDerivativeOfCurl:
#     def test_simple(self, context):
#         f, g, w, element = context.vector(dim=3, cell=tetrahedron)
#         base_expression = curl(f)
#         actual = apply_derivatives(derivative(base_expression, f, w))
#         expected = curl(w)
#         assert equal_up_to_index_relabelling(actual, expected)

# class TestGradientOfDot:
#     def test_simple(self, context):
#         f, g, w, element = context.tensor(dim1=3, dim2=3, cell=triangle)
#         base_expression = dot(f, g)
#         actual = apply_derivatives(grad(base_expression))
#         # We test only that this call actually succeeds.

# class TestGradientOfInner:
#     def test_simple(self, context):
#         f, g, w, element = context.tensor(dim1=3, dim2=2)
#         base_expression = inner(f, g)
#         actual = apply_derivatives(grad(base_expression))
#         # We test only that this call actually succeeds.

# class TestDiv:
#     def test_list_tensor_of_scalars(self, context):
#         f, g, w, element = context.scalar()
#         base_expression = as_tensor([f, g])
#         actual = apply_derivatives(div(base_expression))
#         expected = div(base_expression)
#         assert equal_up_to_index_relabelling(actual, expected)

#     def test_list_tensor_of_vectors(self, context):
#         f, g, w, element = context.vector(dim=3, cell=tetrahedron)
#         base_expression = as_tensor([f, g])
#         assert base_expression.ufl_shape == (2, 3)
#         actual = apply_derivatives(div(base_expression))
#         assert actual.ufl_shape == (2,)
#         expected = as_tensor([div(f), div(g)])
#         assert equal_up_to_index_relabelling(actual, expected)

#     def test_vector_component_tensor(self, context):
#         f, g, w, element = context.vector(dim=3, cell=tetrahedron)
#         ii = MultiIndex((Index(),))
#         base_expression = ComponentTensor(Indexed(f, ii), ii)
#         # Check that no simplification has occurred.
#         assert type(base_expression) == ComponentTensor
#         actual = apply_derivatives(div(base_expression))
#         expected = div(base_expression)
#         assert equal_up_to_index_relabelling(actual, expected)

#     def test_tensor_component_tensor(self, context):
#         # Note here that the Div might in principle pass through the
#         # ComponentTensor, but it does not here for reasons commented
#         # in the implementation.
#         f, g, w, element = context.tensor(dim1=2, dim2=3, cell=tetrahedron)
#         ii, jj = indices(2)
#         iijj = MultiIndex((ii, jj))
#         base_expression = ComponentTensor(Indexed(f, iijj), iijj)
#         # Check that no simplification has occurred.
#         assert type(base_expression) == ComponentTensor
#         actual = apply_derivatives(div(base_expression))
#         expected = div(base_expression)
#         assert equal_up_to_index_relabelling(actual, expected)

#     def test_indexed(self, context):
#         f, g, w, element = context.vector(dim=3, cell=tetrahedron)
#         base_expression = as_tensor([f, g])[1]
#         actual = apply_derivatives(div(base_expression))
#         expected = div(base_expression)
#         assert equal_up_to_index_relabelling(actual, expected)


# class TestCurl:
#     def test_list_tensor(self, context):
#         f, g, w, element = context.scalar(cell=tetrahedron)
#         h = Coefficient(element)
#         base_expression = as_tensor([f, g, h])
#         actual = apply_derivatives(curl(base_expression))
#         expected = curl(base_expression)
#         assert equal_up_to_index_relabelling(actual, expected)

#     def test_component_tensor(self, context):
#         f, g, w, element = context.vector(dim=3, cell=tetrahedron)
#         ii = MultiIndex((Index(),))
#         base_expression = ComponentTensor(Indexed(f, ii), ii)
#         # Check that no simplification has occurred.
#         assert type(base_expression) == ComponentTensor
#         actual = apply_derivatives(curl(base_expression))
#         expected = curl(base_expression)
#         assert equal_up_to_index_relabelling(actual, expected)

#     def test_indexed(self, context):
#         f, g, w, element = context.vector(dim=3, cell=tetrahedron)
#         base_expression = as_tensor([f, g])[1]
#         actual = apply_derivatives(curl(base_expression))
#         expected = curl(base_expression)
#         assert equal_up_to_index_relabelling(actual, expected)


# class TestCombined:
#     def test_dot_grad(self, context):
#         f, g, w, element = context.scalar()
#         base_expression = dot(grad(f), grad(g))
#         actual = apply_derivatives(derivative(base_expression, f, w))
#         expected = dot(grad(w), grad(g))
#         assert equal_up_to_index_relabelling(actual, expected)

#     def test_dot_grad_multiply(self, context):
#         f, g, w, element = context.scalar()
#         base_expression = dot(grad(f), f * grad(g))
#         actual = apply_derivatives(derivative(base_expression, f, w))
#         expected = dot(grad(w), f * grad(g)) + dot(grad(f), w * grad(g))
#         assert equal_up_to_index_relabelling(actual, expected)

#     def test_specified_coefficient_derivatives(self, context):
#         f, g, w, element = context.scalar()
#         base_expression = dot(grad(f), grad(g))
#         h = Coefficient(element)
#         df = Coefficient(element)
#         dg = Coefficient(element)
#         actual = apply_derivatives(derivative(base_expression, h, w, {f: df, g:dg}))
#         # The expected result is really
#         # dot(grad(w)*df + w*grad(df), grad(g))
#         # + dot(grad(f), grad(w)*dg + w*grad(dg))
#         # But, when expanded, this gives something involving sums of
#         # component tensors, while the actual result has component
#         # tensors of sums. Accordingly, we have to expand this
#         # ourselves.
#         expected = (
#             dot(ComponentTensor(Indexed(grad(w), MultiIndex((i,)))*df
#                                 + w*Indexed(grad(df), MultiIndex((i,))),
#                                 MultiIndex((i,))),
#                 grad(g))
#             + dot(grad(f),
#                   ComponentTensor(Indexed(grad(w), MultiIndex((i,)))*dg
#                                   + w*Indexed(grad(dg), MultiIndex((i,))),
#                                   MultiIndex((i,))))
#             )
#         assert equal_up_to_index_relabelling(actual, expected)

#     def test_inner_grad(self, context):
#         f, g, w, element = context.tensor(dim1=2, dim2=3)
#         base_expression = inner(grad(f), grad(g))
#         actual = apply_derivatives(derivative(base_expression, f, w))
#         expected = inner(grad(w), grad(g))
#         assert equal_up_to_index_relabelling(actual, expected)

#     def test_component_derivative(self):
#         # Simpler test of a use-case shown first by
#         # test_derivative::test_segregated_derivative_of_convection.
#         cell = triangle
#         V = FiniteElement("CG", cell, 1)
#         W = VectorElement("CG", cell, 1, dim=2)
#         u = Coefficient(W)
#         v = Coefficient(W)
#         du = TrialFunction(V)

#         L = inner(grad(u), grad(v))
#         dL = derivative(L, u[0], du)
#         form = dL * dx
#         fd = compute_form_data(form)
#         pf = fd.preprocessed_form
#         a = expand_indices(pf) # This test exists to ensure that this call does not cause an exception.

#     def test_component_derivative_simple(self):
#         cell = triangle
#         vector_element = VectorElement("CG", cell, 1, dim=3)
#         scalar_element = FiniteElement("CG", cell, 1)
#         u = Coefficient(vector_element)
#         w = Argument(scalar_element, 0)
#         base_expression = derivative(grad(u), u[0], w)
#         actual = apply_derivatives(base_expression)
#         zero_2d = Zero((2,), (), ())
#         expected = as_tensor([grad(w), zero_2d, zero_2d])
#         assert equal_up_to_index_relabelling(actual, expected)

#     def test_derivative_wrt_tuple(self):
#         cell = triangle
#         scalar_element = FiniteElement("CG", cell, degree=1)
#         f = Coefficient(scalar_element)
#         g = Coefficient(scalar_element)
#         vector_element = VectorElement("CG", cell, degree=1, dim=2)
#         w = Argument(vector_element, 0)
#         base_expression = dot(grad(f), grad(g))
#         actual = apply_derivatives(derivative(base_expression, (f, g), w))
#         expected = dot(grad(w[0]), grad(g)) + dot(grad(f), grad(w[1]))
#         expected = apply_derivatives(expected) # Push grads inside indexing.
#         assert equal_up_to_index_relabelling(actual, expected)

#     def test_grad_spatial_coordinate_shape(self, context):
#         # Checks that the geometric dimension assigned to GradRuleset
#         # in DerivativeRuleDispatcher is correct.
#         cell = tetrahedron
#         element = VectorElement("CG", cell, degree=1, dim=2)
#         x = SpatialCoordinate(element.cell()) # shape: (3,)
#         y = Coefficient(element) # (2,)
#         w = grad(grad(y)) # (2, 3, 3)
#         z = dot(w, x) # (2, 3)
#         expr = grad(z) # (2, 3, 3)
#         assert expr.ufl_shape == (2, 3, 3)
#         expr = apply_derivatives(expr)
#         assert expr.ufl_shape == (2, 3, 3)

# class TestCancellations:
#     def compute_form_data_with_pullbacks(self, expr):
#         integral = expr * dx
#         form_data = compute_form_data(
#             integral,
#             do_apply_function_pullbacks=True)
#         return form_data.preprocessed_form._integrals[0].integrand()

#     def transform(self, expr):
#         # GTODO: Check that this matches compute_form_data.
#         # GTODO: Merge this with the functions above and below.
#         expr = apply_minimal_algebra_lowering(expr)
#         expr = apply_derivatives(expr)
#         expr = apply_function_pullbacks(expr)
#         expr = apply_derivatives(expr)
#         expr = apply_jacobian_cancellation(expr)
#         expr = apply_algebra_lowering(expr)
#         expr = apply_derivatives(expr)
#         return expr


#     def test_div_div_nonconforming(self, context):
#         f, g, w, element = context.vector(dim=3, cell=tetrahedron)
#         base_expression = div(f)
#         actual = self.compute_form_data_with_pullbacks(base_expression)
#         expected = IndexSum(
#             Indexed(ComponentTensor(
#                 IndexSum(Product(
#                     Indexed(
#                         JacobianInverse(f.ufl_domain()),
#                         MultiIndex((Index(43), Index(42)))),
#                     Indexed(ReferenceGrad(ReferenceValue(f)),
#                             MultiIndex((Index(41), Index(43))))),
#                          MultiIndex((Index(43),))),
#                 MultiIndex((Index(41), Index(42)))),
#                     MultiIndex((Index(40), Index(40)))),
#             MultiIndex((Index(40),)))
#         assert equal_up_to_index_relabelling(actual, expected)

#     def test_div_div_conforming(self, context):
#         f, g, w, element = context.rt()
#         base_expression = div(f)
#         actual = self.compute_form_data_with_pullbacks(base_expression)
#         mesh = f.ufl_domain()
#         expected = apply_algebra_lowering((1.0)/JacobianDeterminant(mesh) * ReferenceDiv(ReferenceValue(f)))
#         explicit_expected = Product(Division(FloatValue(1.0), JacobianDeterminant(mesh)),
#                                     IndexSum(Indexed(ReferenceGrad(ReferenceValue(f)), MultiIndex((Index(13), Index(13)))),
#                                              MultiIndex((Index(13),))))
#         assert equal_up_to_index_relabelling(actual, expected)
#         assert equal_up_to_index_relabelling(actual, explicit_expected)

#     def test_curl_covariant_Piola(self, context):
#         f, g, w, element = context.n1curl()
#         base_expression = curl(f)
#         actual = self.transform(base_expression)
#         domain = f.ufl_domain()
#         J = Jacobian(domain)
#         detJ = JacobianDeterminant(domain)
#         expected = apply_derivatives(
#             apply_algebra_lowering(
#                 1.0/detJ * dot(J, ReferenceCurl(ReferenceValue(f)))))
#         assert equal_up_to_index_relabelling(actual, expected)


# def transform(expr):
#     form = expr * dx
#     form_data = compute_form_data(form, do_apply_function_pullbacks=True)
#     return form_data.preprocessed_form.integrals()[0]._integrand
#     # # Transform as for compute_form_data with
#     # # do_apply_function_pullbacks=True
#     # expr = apply_minimal_algebra_lowering(expr)
#     # expr = apply_derivatives(expr)
#     # expr = apply_function_pullbacks(expr)
#     # expr = apply_integral_scaling(expr)
#     # expr = apply_algebra_lowering(expr)
#     # expr = apply_derivatives(expr)
#     # return expr
        
# class TestPullbacks():
#     def test_grad_pullback(self, context):
#         f, g, w, element = context.vector(dim=3, cell=triangle)
#         base_expression = inner(grad(f), grad(g))
#         actual = transform(base_expression)
#         K = JacobianInverse(f.ufl_domain()) # Mesh(VectorElement(FiniteElement('Lagrange', triangle, 1), dim=2), -1))
#         expected = inner(dot(ReferenceGrad(ReferenceValue(f)), K),
#                          dot(ReferenceGrad(ReferenceValue(g)), K))
#         expected = apply_algebra_lowering(expected)
#         assert equal_up_to_index_relabelling(actual, expected)

#     def test_div_conforming_identity(self):
#         cell = triangle
#         rt_element = FiniteElement("RT", cell, degree=1)
#         cg_element = FiniteElement("CG", cell, degree=1)
#         q = Coefficient(rt_element)
#         v = Coefficient(cg_element)
#         base_expression = dot(q, grad(v))
#         actual = transform(base_expression)
#         detJ = JacobianDeterminant(q.ufl_domain())
#         expected = apply_algebra_lowering(
#             dot((1.0/detJ) * ReferenceValue(q),
#                 ReferenceGrad(ReferenceValue(v))))
#         assert equal_up_to_index_relabelling(actual, expected)

#     def test_div_conforming_identity_reversed(self):
#         # Identical to test_div_conforming_identity except for the
#         # order of the operands to the dot product.
#         cell = triangle
#         rt_element = FiniteElement("RT", cell, degree=1)
#         cg_element = FiniteElement("CG", cell, degree=1)
#         q = Coefficient(rt_element)
#         v = Coefficient(cg_element)
#         base_expression = dot(grad(v), q)
#         actual = transform(base_expression)
#         detJ = JacobianDeterminant(q.ufl_domain())
#         expected = apply_algebra_lowering(
#             dot((1.0/detJ) * ReferenceValue(q),
#                 ReferenceGrad(ReferenceValue(v))))
#         assert equal_up_to_index_relabelling(actual, expected)

#     def test_curl_conforming_identity(self):
#         cell = triangle
#         rt_element = FiniteElement("RT", cell, degree=1)
#         n_element = FiniteElement("N1curl", cell, degree=1)
#         q = Coefficient(rt_element)
#         chi = Coefficient(n_element)
#         base_expression = dot(q, chi)
#         actual = transform(base_expression)
#         detJ = JacobianDeterminant(q.ufl_domain())
#         expected = apply_algebra_lowering(
#             dot((1.0/detJ) * ReferenceValue(q),
#                 ReferenceValue(chi)))
#         assert equal_up_to_index_relabelling(actual, expected)

#     def test_curl_conforming_identity_reversed(self):
#         # Identical to test_curl_conforming_identity except for the
#         # order of the operands to the dot product.
#         cell = triangle
#         rt_element = FiniteElement("RT", cell, degree=1)
#         n_element = FiniteElement("N1curl", cell, degree=1)
#         q = Coefficient(rt_element)
#         chi = Coefficient(n_element)
#         base_expression = dot(chi, q)
#         actual = transform(base_expression)
#         detJ = JacobianDeterminant(q.ufl_domain())
#         expected = apply_algebra_lowering(
#             dot((1.0/detJ) * ReferenceValue(q),
#                 ReferenceValue(chi)))
#         assert equal_up_to_index_relabelling(actual, expected)

#     def test_sum_as_cutoff_type_1(self):
#         cell = triangle
#         rt_element = FiniteElement("RT", cell, degree=1)
#         cg_element = FiniteElement("CG", cell, degree=1)
#         q1 = Coefficient(rt_element)
#         q2 = Coefficient(rt_element)
#         v1 = Coefficient(cg_element)
#         v2 = Coefficient(cg_element)
#         base_expression = dot(q1, grad(v1)) + dot(grad(v2), q2)
#         actual = transform(base_expression)
#         detJ = JacobianDeterminant(q1.ufl_domain())
#         expected = apply_algebra_lowering(
#             dot((1.0/detJ) * ReferenceValue(q1),
#                 ReferenceGrad(ReferenceValue(v1)))
#             + dot((1.0/detJ) * ReferenceValue(q2),
#                 ReferenceGrad(ReferenceValue(v2))))
#         assert equal_up_to_index_relabelling(actual, expected)

#     def test_sum_as_cutoff_type_2(self):
#         cell = triangle
#         rt_element = FiniteElement("RT", cell, degree=1)
#         cg_element = FiniteElement("CG", cell, degree=1)
#         q1 = Coefficient(rt_element)
#         q2 = Coefficient(rt_element)
#         v1 = Coefficient(cg_element)
#         v2 = Coefficient(cg_element)
#         base_expression = dot(q1 + q2, grad(v1) + grad(v2))
#         actual = transform(base_expression)
#         detJ = JacobianDeterminant(q1.ufl_domain())
#         expected = apply_algebra_lowering(
#             dot((1.0/detJ) * ReferenceValue(q1)
#                 + (1.0/detJ) * ReferenceValue(q2),
#                 ReferenceGrad(ReferenceValue(v1))
#                 + ReferenceGrad(ReferenceValue(v2))))
#         assert equal_up_to_index_relabelling(actual, expected)

#     def test_sum_as_cutoff_type_3(self):
#         cell = triangle
#         rt_element = FiniteElement("RT", cell, degree=1)
#         cg_element = FiniteElement("CG", cell, degree=1)
#         q1 = Coefficient(rt_element)
#         q2 = Coefficient(rt_element)
#         v1 = Coefficient(cg_element)
#         v2 = Coefficient(cg_element)
#         base_expression = dot(grad(v1) + grad(v2), q1 + q2)
#         actual = transform(base_expression)
#         detJ = JacobianDeterminant(q1.ufl_domain())
#         expected = apply_algebra_lowering(
#             dot((1.0/detJ) * ReferenceValue(q1)
#                 + (1.0/detJ) * ReferenceValue(q2),
#                 ReferenceGrad(ReferenceValue(v1))
#                 + ReferenceGrad(ReferenceValue(v2))))
#         assert equal_up_to_index_relabelling(actual, expected)

#     @pytest.mark.xfail
#     def test_div_conforming_identity_with_split(self):
#         cell = triangle
#         rt_element = FiniteElement("RT", cell, degree=1)
#         cg_element = FiniteElement("CG", cell, degree=1)
#         element = MixedElement(rt_element, cg_element)
#         coeff = Coefficient(element)
#         q, v = split(coeff)
#         base_expression = dot(q, grad(v))
#         actual = transform(base_expression)
#         detJ = JacobianDeterminant(q.ufl_domain())
#         ref_q = as_tensor([ReferenceValue(coeff)[0],
#                            ReferenceValue(coeff)[1]])
#         ref_v = ReferenceValue(coeff)[2]
#         expected = apply_algebra_lowering(
#             dot((1.0/detJ) * ref_q,
#                 ReferenceGrad(ref_v)))
#         assert equal_up_to_index_relabelling(actual, expected)
