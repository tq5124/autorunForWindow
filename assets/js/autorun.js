(function(){
  var app = angular.module('autorunModule', []);

  app.config(function(){

  });

  app.controller('MasterCtrl', function($scope, $http){
    $scope.outputs = {
      "logon": logon,
      "services": services,
      "internetExplorer": internetExplorer
    };

    $scope.tab = "";
    $scope.tabData = "";

    $scope.changeTab = function(tab){
      $scope.tab = tab;
      $scope.tabData = $scope.outputs[tab];
    };
  });

})();
