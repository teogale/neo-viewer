
describe("neo-visualizer fonction test", function() {
    var $scope;
    var $controller;
    beforeEach(angular.mock.module('neo-visualizer'));
    

    beforeEach(inject(angular.mock.inject(function(_$rootScope_, _$controller_) {
     
      $rootScope = _$rootScope_;
      $scope = $rootScope.$new();
      $controller = _$controller_;
      controller = $controller('MainCtrl', { $scope: $scope });
    })));

    it("controller should be define",function(){
      expect(controller).toBeDefined();
    });
  
    // it('meh',function(){
    //   $scope.source = "https://github.com/teogale/test_file_api/raw/master/96711008.abf";
    //   $scope.currentSegmentId = 0;
    //   $scope.currentAnalogSignalId = 0;
    //   $scope.downsamplefactor = 1;
    //   $scope.iotype = "";
    //   $scope.showMultiChannelSignal();
    //   
    // });
    
  

  });