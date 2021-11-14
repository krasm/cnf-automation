vf-modules = apache
.PHONY: build clean $(vf-modules:=-build) $(vf-modules:-clean) $(vf-modules:=-package)

package: $(vf-modules:=-package)
build: $(vf-modules:=-build)
clean: $(vf-modules:=-clean)

$(vf-modules:=-package): %-package: %-build
	mv $(@:package=)*.tgz helm_$(@:-package=).tgz

$(vf-modules:=-build): %-build: %-clean
	helm package $(@:-build=)

$(vf-modules:=-clean):
	rm -f $(@:-clean=)-*.tgz
	rm -f helm_$(@:-clean=).tgz
