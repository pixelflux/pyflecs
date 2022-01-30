/* Copyright (c) 2022 Pixel Flux
 *
 * Permission is hereby granted, free of charge, to any person obtaining
 * a copy of this software and associated documentation files (the
 * "Software"), to deal in the Software without restriction, including
 * without limitation the rights to use, copy, modify, merge, publish,
 * distribute, sublicense, and/or sell copies of the Software, and to
 * permit persons to whom the Software is furnished to do so, subject to
 * the following conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
 * IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
 * CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
 * TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 * SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

#include "filter.hpp"

using namespace pyflecs;

filter_iter::filter_iter(ecs_iter_t iter) : 
    mRaw(iter)
{

}

bool filter_iter::next()
{
    return ecs_iter_next(&mRaw);
}

void* filter_iter::term(entity& e, int32_t idx)
{
    return ecs_term_w_size(&mRaw, e.size(), idx);
}


filter::filter(ecs_world_t* world, ecs_filter_t f) :
    mpWorld(world),
    mRaw(f)
{

}

filter_iter filter::iter()
{
    return filter_iter(ecs_filter_iter(mpWorld, &mRaw));
}
