#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include "Attributes/WireAttributeTest.h"
#include "Attributes/WireEdgeCubicSymmetryAttributeTest.h"
#include "Attributes/WireEdgePeriodicIndexAttributeTest.h"
#include "Attributes/WireEdgeSymmetryAttributeTest.h"
#include "Attributes/WireVertexCubicSymmetryAttributeTest.h"
#include "Attributes/WireVertexMinAngleAttributeTest.h"
#include "Attributes/WireVertexPeriodicIndexAttributeTest.h"
#include "Attributes/WireVertexSupportAttributeTest.h"
#include "Attributes/WireVertexSymmetryAttributeTest.h"
#include "Inflator/AABBTreeTest.h"
#include "Inflator/IsotropicPeriodicInflatorTest.h"
#include "Inflator/GeometryCorrectionTableTest.h"
#include "Inflator/PeriodicInflator2DTest.h"
#include "Inflator/PeriodicInflator3DTest.h"
#include "Inflator/PhantomMeshGeneratorTest.h"
#include "Inflator/SimpleInflatorTest.h"
#include "Inflator/WireProfileTest.h"
#include "Interfaces/PeriodicExplorationTest.h"
#include "Misc/BilinearInterpolationTest.h"
#include "Misc/BoundaryRemesherTest.h"
#include "Misc/BoxCheckerTest.h"
#include "Misc/DistanceComputationTest.h"
#include "Misc/EdgeSplitterTest.h"
#include "Misc/SymmetryOperatorsTest.h"
#include "Misc/TrilinearInterpolationTest.h"
#include "Parameters/IsotropicDofExtractorTest.h"
#include "Parameters/IsotropicTransformsTest.h"
#include "Parameters/ThicknessParametersTest.h"
#include "Parameters/OffsetParameterTest.h"
#include "Parameters/ParameterManagerTest.h"
#include "Parameters/SymmetryOrbitsTest.h"
#include "Parameters/EdgeThicknessParameterDerivativeTest.h"
#include "Parameters/VertexOffsetParameterDerivativeTest.h"
#include "Parameters/VertexThicknessParameterDerivativeTest.h"
#include "Tiler/AABBTilerTest.h"
#include "Tiler/MeshTilerTest.h"
#include "Tiler/MixedMeshTilerTest.h"
#include "WireNetwork/WireConnectivityTest.h"
#include "WireNetwork/WireNetworkTest.h"

int main(int argc, char** argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
